from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from decimal import Decimal
from datetime import datetime
import uuid
from typing import Optional

from src.database.database import get_db  # Your database session dependency
from src.models.wallet import Wallet
from src.models.transaction import Transaction

router = APIRouter(prefix="/payments", tags=["payments"])


class PaymentRequest(BaseModel):
    from_wallet_number: str
    to_wallet_number: str
    amount: float
    description: Optional[str] = None

    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v


class PaymentResponse(BaseModel):
    transaction_id: int
    reference_code: str
    status: str
    message: str


@router.post("/", response_model=PaymentResponse)
async def create_payment(
        payment: PaymentRequest,
        db: Session = Depends(get_db)
):
    # Get wallets
    from_wallet = db.query(Wallet).filter(Wallet.wallet_number == payment.from_wallet_number).first()
    to_wallet = db.query(Wallet).filter(Wallet.wallet_number == payment.to_wallet_number).first()

    if not from_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source wallet not found"
        )

    if not to_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination wallet not found"
        )

    if from_wallet.id == to_wallet.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot transfer to the same wallet"
        )

    # Check wallet status
    if from_wallet.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source wallet is not active"
        )

    if to_wallet.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Destination wallet is not active"
        )

    # Check sufficient balance
    payment_amount = Decimal(str(payment.amount))
    if from_wallet.balance < payment_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )

        # Generate reference code
    reference_code = f"PAY{uuid.uuid4().hex[:8].upper()}"

    try:
        # Create transaction
        transaction = Transaction(
            from_wallet_id=from_wallet.id,
            to_wallet_id=to_wallet.id,
            amount=payment_amount,
            description=payment.description or f"Payment to {to_wallet.wallet_number}",
            reference_code=reference_code,
            status="completed"
        )

        # Update balances
        from_wallet.balance -= payment_amount
        to_wallet.balance += payment_amount
        from_wallet.updated_at = datetime.utcnow()
        to_wallet.updated_at = datetime.utcnow()

        # Set processed timestamp
        transaction.processed_at = datetime.utcnow()

        # Save to database
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return PaymentResponse(
            transaction_id=transaction.id,
            reference_code=reference_code,
            status="completed",
            message="Payment completed successfully"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Payment failed"
        )