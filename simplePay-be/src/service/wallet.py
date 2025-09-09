import time
import uuid
from datetime import datetime
from decimal import Decimal
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from src.database.database import get_db
from src.models import User, Wallet, Transaction, Base
from src.schemas.wallet import WithdrawRequest, OperationResponse, DepositRequest

def mock_card_payment(card_number: str, _: Decimal) -> bool:
    time.sleep(1)

    test_fail_cards = ["4000000000000002", "4000000000000010"]
    if card_number in test_fail_cards:
        return False

    return True


def mock_bank_transfer(bank_account: str,  _: Decimal) -> bool:
    time.sleep(2)

    test_fail_accounts = ["IT60X0542811101000000123456"]
    if bank_account in test_fail_accounts:
        return False

    return True

class WalletService:
    @staticmethod
    def create_wallet(db: Session, user_id: int):
        wallet_number = f"SP{str(uuid.uuid4().int)[:12]}"
        db_wallet = Wallet(
            user_id=user_id,
            wallet_number=wallet_number,
            balance=0.00,
            status="active",
            currency="EUR"
        )

        try:
            db.add(db_wallet)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Wallet creation error: {str(e)}")

    @staticmethod
    def withdraw_from_wallet(
            withdraw: WithdrawRequest,
            current_user: User,
            db: Session = Depends(get_db)
    ):
        user_wallet: Wallet(Base) = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()

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

        if user_wallet.balance < withdraw_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )

        transfer_success = mock_bank_transfer(withdraw.bank_account, withdraw.amount)

        if not transfer_success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bank transfer failed"
            )

        reference_code = f"WTH{uuid.uuid4().hex[:8].upper()}"

        try:
            transaction = Transaction(
                from_wallet_id=user_wallet.id,
                to_wallet_id=None,
                amount=withdraw_amount,
                description=f"Bank withdrawal - {withdraw.back_account_name}",
                reference_code=reference_code,
                status="completed",
                transaction_type="withdraw"
            )

            user_wallet.withdraw(withdraw_amount)

            transaction.processed_at = datetime.utcnow()

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

    @staticmethod
    def deposit_to_wallet(
            deposit: DepositRequest,
            current_user: User,
            db: Session = Depends(get_db)
    ):
        # Get user wallet
        user_wallet: Wallet(Base) = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()

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

        payment_success = mock_card_payment(deposit.card_number, deposit.amount)

        if not payment_success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Card payment failed"
            )

        reference_code = f"TOP{uuid.uuid4().hex[:8].upper()}"

        try:
            transaction = Transaction(
                from_wallet_id=None,
                to_wallet_id=user_wallet.id,
                amount=deposit_amount,
                description=f"Card deposit - **** {deposit.card_number[-4:]}",
                reference_code=reference_code,
                status="completed",
                transaction_type="deposit"
            )

            user_wallet.deposit(deposit_amount)

            transaction.processed_at = datetime.utcnow()

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

    @staticmethod
    def get_wallet(current_user: User,
            db: Session = Depends(get_db)) -> Wallet:
        return db.query(Wallet).filter(Wallet.user_id == current_user.id).first()