from operator import and_
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime
import uuid
from typing import Optional
from src.schemas.payments import PaymentRequest, PaymentResponse
from src.models import User, Base
from src.models.wallet import Wallet
from src.models.transaction import Transaction

class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    def exchange_money(self,
                       payment: PaymentRequest,
                       current_user: User):

        from_wallet: Wallet(Base) = self.db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
        to_wallet: Wallet(Base) = self.db.query(Wallet).join(User, Wallet.user_id == User.id).filter(
            User.email == payment.to_user_email).first()

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

        payment_amount = Decimal(str(payment.amount))
        if from_wallet.balance < payment_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )

        reference_code = f"PAY{uuid.uuid4().hex[:8].upper()}"

        try:
            transaction_user_from = TransactionService(self.db).create_transaction(
                from_wallet_id=from_wallet.id,
                to_wallet_id=to_wallet.id,
                amount=payment_amount,
                description=f"Payment to {payment.to_user_email}",
                transaction_type="send",
            )

            transaction_user_to = TransactionService(self.db).create_transaction(
                from_wallet_id=to_wallet.id,
                to_wallet_id=from_wallet.id,
                amount=payment_amount,
                description=f"Receiving from {current_user.email}",
                transaction_type="receive",
            )

            from_wallet.withdraw(payment_amount)
            to_wallet.deposit(payment_amount)

            transaction_user_from.processed_at = datetime.utcnow()
            transaction_user_to.processed_at = datetime.utcnow()

            self.db.add(transaction_user_from)
            self.db.add(transaction_user_to)
            self.db.commit()
            self.db.refresh(transaction_user_from)
            self.db.refresh(transaction_user_to)

            return PaymentResponse(
                reference_code=reference_code,
                status="completed",
                message="Payment completed successfully"
            )

        except Exception as e:
            self.db.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Payment failed"
            )


    def get_transactions_paginated(self, 
                                   current_user: User,
                                   page: int = Query(1, ge=1),
                                   page_size: int = Query(10, ge=1, le=100),
                                   search: Optional[str] = Query(None,
                                                                 description="Search by description, reference code or type"),
                                   start_date: Optional[datetime] = Query(None,
                                                                          description="Filter start date (format: YYYY-MM-DD)"),
                                   end_date: Optional[datetime] = Query(None,
                                                                        description="Filter end date (format: YYYY-MM-DD)"),
                                   ):
        wallet = self.db.query(Wallet).filter(Wallet.user_id == current_user.id).first()

        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        query = self.db.query(Transaction).filter(
            or_(
                and_(Transaction.from_wallet_id == wallet.id, Transaction.transaction_type == "send"),
                and_(Transaction.from_wallet_id == wallet.id, Transaction.transaction_type == "receive"),
                and_(Transaction.to_wallet_id == wallet.id,
                     and_(Transaction.from_wallet_id.is_(None), Transaction.transaction_type == "deposit")),
                and_(Transaction.from_wallet_id == wallet.id,
                     and_(Transaction.to_wallet_id.is_(None), Transaction.transaction_type == "withdraw"))
            )
        )

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Transaction.description.ilike(search_term),
                    Transaction.reference_code.ilike(search_term),
                    Transaction.transaction_type.ilike(search_term)
                )
            )

        if start_date:
            start_of_day = datetime.combine(start_date.date(), datetime.min.time())
            query = query.filter(Transaction.created_at >= start_of_day)
        if end_date:
            end_of_day = datetime.combine(end_date.date(), datetime.max.time())
            query = query.filter(Transaction.created_at <= end_of_day)

        total = query.count()
        transactions = query.order_by(Transaction.created_at.desc()).offset((page - 1) * page_size).limit(
            page_size).all()

        return {
            "data": transactions,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size
        }

    def create_transaction(
            self,
            from_wallet_id: Optional[int],
            to_wallet_id: Optional[int],
            amount: Decimal,
            transaction_type: str,
            description: str = "",
    ) -> Transaction:
        reference_code = f"TXN{uuid.uuid4().hex[:8].upper()}"

        try:
            transaction = Transaction(
                from_wallet_id=from_wallet_id,
                to_wallet_id=to_wallet_id,
                amount=amount,
                description=description,
                reference_code=reference_code,
                status="completed",
                transaction_type=transaction_type,
            )

            self.db.add(transaction)
            self.db.commit()
            self.db.refresh(transaction)
            return transaction
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Transaction creation failed: {str(e)}"
            )