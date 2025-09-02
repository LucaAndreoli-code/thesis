from typing import Any, Coroutine

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from decimal import Decimal
from datetime import datetime
import uuid
import random
import time
from src.database.database import get_db
from src.models.user import User
from src.models.wallet import Wallet
from src.models.transaction import Transaction
from src.service.auth import get_current_user

router = APIRouter(prefix="/wallet", tags=["Wallet"])

class DepositRequest(BaseModel):
    amount: float
    card_number: str
    card_holder: str
    expiry_month: int
    expiry_year: int
    cvv: str

    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0 or v > 10000:  # Max 10k per transaction
            raise ValueError('Amount must be between 0 and 10000')
        return v

    @field_validator('card_number')
    def validate_card_number(cls, v):
        # Basic card number validation (remove spaces)
        card_clean = v.replace(" ", "")
        if not card_clean.isdigit() or len(card_clean) != 16:
            raise ValueError('Invalid card number format')
        return card_clean


class WithdrawRequest(BaseModel):
    amount: float
    bank_account: str
    back_account_name: str

    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0 or v > 50000:  # Max 50k per transaction
            raise ValueError('Amount must be between 0 and 50000')
        return v


class OperationResponse(BaseModel):
    transaction_id: int
    reference_code: str
    status: str
    message: str
    new_balance: str


def mock_card_payment(card_number: str, amount: float) -> bool:
    time.sleep(1)  # Simulate processing time

    # Simulate failure for some test cards
    test_fail_cards = ["4000000000000002", "4000000000000010"]
    if card_number in test_fail_cards:
        return False

    # Random 5% failure rate for realistic simulation
    return random.random() > 0.05


def mock_bank_transfer(bank_account: str, amount: float) -> bool:
    time.sleep(2)  # Simulate processing time

    # Simulate failure for some test accounts
    test_fail_accounts = ["IT60X0542811101000000123456"]
    if bank_account in test_fail_accounts:
        return False

    # Random 3% failure rate
    return random.random() > 0.03


@router.post("/deposit", response_model=OperationResponse)
async def deposit_wallet(
        deposit: DepositRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Get user wallet
    user_wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()

    if not user_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

    if user_wallet.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wallet is not active"
        )

    deposit_amount = Decimal(str(deposit.amount))

    # Mock card payment processing
    payment_success = mock_card_payment(deposit.card_number, deposit.amount)

    if not payment_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Card payment failed"
        )

    # Generate reference code
    reference_code = f"TOP{uuid.uuid4().hex[:8].upper()}"

    try:
        # Create transaction record (from external system to user wallet)
        transaction = Transaction(
            from_wallet_id=user_wallet.id,  # Using same wallet as placeholder
            to_wallet_id=user_wallet.id,
            amount=deposit_amount,
            description=f"Card deposit - **** {deposit.card_number[-4:]}",
            reference_code=reference_code,
            status="completed",
            transaction_type="deposit"
        )

        # Update wallet balance
        user_wallet.balance += deposit_amount
        user_wallet.updated_at = datetime.utcnow()

        # Set processed timestamp
        transaction.processed_at = datetime.utcnow()

        # Save to database
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return OperationResponse(
            transaction_id=transaction.id,
            reference_code=reference_code,
            status="completed",
            message="Deposit completed successfully",
            new_balance=str(user_wallet.balance)
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Deposit failed"
        )


@router.post("/withdraw", response_model=OperationResponse)
async def withdraw_from_wallet(
        withdraw: WithdrawRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Get user wallet
    user_wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()

    if not user_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

    if user_wallet.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wallet is not active"
        )

    withdraw_amount = Decimal(str(withdraw.amount))

    # Check sufficient balance
    if user_wallet.balance < withdraw_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )

    # Mock bank transfer processing
    transfer_success = mock_bank_transfer(withdraw.bank_account, withdraw.amount)

    if not transfer_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bank transfer failed"
        )

    # Generate reference code
    reference_code = f"WTH{uuid.uuid4().hex[:8].upper()}"

    try:
        # Create transaction record (from user wallet to external system)
        transaction = Transaction(
            from_wallet_id=user_wallet.id,
            to_wallet_id=user_wallet.id,  # Using same wallet as placeholder
            amount=withdraw_amount,
            description=f"Bank withdrawal - {withdraw.back_account_name}",
            reference_code=reference_code,
            status="completed",
            transaction_type="withdraw"
        )

        # Update wallet balance
        user_wallet.balance -= withdraw_amount
        user_wallet.updated_at = datetime.utcnow()

        # Set processed timestamp
        transaction.processed_at = datetime.utcnow()

        # Save to database
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return OperationResponse(
            transaction_id=transaction.id,
            reference_code=reference_code,
            status="completed",
            message="Withdrawal completed successfully",
            new_balance=str(user_wallet.balance)
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Withdrawal failed"
        )

class BalanceResponse(BaseModel):
    balance: Decimal
    currency: str

@router.get("/balance", response_model=BalanceResponse)
async def get_wallet_balance(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> dict[str, Any]:
    user_wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()

    if not user_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

    return {
        "balance": user_wallet.balance,
        "currency": user_wallet.currency
    }