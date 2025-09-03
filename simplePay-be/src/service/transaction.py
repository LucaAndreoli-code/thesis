from operator import and_
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime
import uuid
from typing import Optional
from src.schemas.payments import PaymentRequest, PaymentResponse
from src.database.database import get_db
from src.models import User, Base
from src.models.wallet import Wallet
from src.models.transaction import Transaction
from src.service.auth import AuthService

class TransactionService:
    @staticmethod
    def exchange_money(payment: PaymentRequest,
        current_user:User=Depends(AuthService.get_current_user),
        db: Session = Depends(get_db)):

        # Get wallets
        from_wallet: Wallet(Base) = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
        to_wallet: Wallet(Base) = db.query(Wallet).join(User, Wallet.user_id == User.id).filter(
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
            transaction_user_from = Transaction(
                from_wallet_id=from_wallet.id,
                to_wallet_id=to_wallet.id,
                amount=payment_amount,
                description=f"Payment to {payment.to_user_email}",
                reference_code=reference_code,
                status="completed",
                transaction_type="send"
            )

            transaction_user_to = Transaction(
                from_wallet_id=to_wallet.id,
                to_wallet_id=from_wallet.id,
                amount=payment_amount,
                description=f"Receiving from {current_user.email}",
                reference_code=reference_code,
                status="completed",
                transaction_type="receive"
            )

            # Update balances
            from_wallet.withdraw(payment_amount)
            to_wallet.deposit(payment_amount)

            # Set processed timestamp
            transaction_user_from.processed_at = datetime.utcnow()
            transaction_user_to.processed_at = datetime.utcnow()

            # Save to database
            TransactionService.create_transaction(db, transaction_user_from)
            TransactionService.create_transaction(db, transaction_user_to)

            return PaymentResponse(
                reference_code=reference_code,
                status="completed",
                message="Payment completed successfully"
            )

        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Payment failed"
            )

    @staticmethod
    def get_transactions(page: int = Query(1, ge=1),
                        page_size: int = Query(10, ge=1, le=100),
                        search: Optional[str] = Query(None,
                                                      description="Ricerca per descrizione, codice riferimento o tipo"),
                        start_date: Optional[datetime] = Query(None,
                                                               description="Data di inizio filtro (formato: YYYY-MM-DD)"),
                        end_date: Optional[datetime] = Query(None,
                                                             description="Data di fine filtro (formato: YYYY-MM-DD)"),
                        db: Session = Depends(get_db),
                        current_user: User = Depends(AuthService.get_current_user)):
        wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()

        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        query = db.query(Transaction).filter(
            or_(
                # Caso 1: Ho mandato io soldi (send)
                and_(Transaction.from_wallet_id == wallet.id, Transaction.transaction_type == "send"),
                # Caso 2: Ho ricevuto io soldi (receive)
                and_(Transaction.from_wallet_id == wallet.id, Transaction.transaction_type == "receive"),
                # Caso 3: Ho depositato soldi (deposit)
                and_(Transaction.to_wallet_id == wallet.id,
                     and_(Transaction.from_wallet_id.is_(None), Transaction.transaction_type == "deposit")),
                # Caso 4: Ho prelevato soldi (withdraw)
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
            query = query.filter(Transaction.created_at >= start_date)
        if end_date:
            query = query.filter(Transaction.created_at <= end_date)

        total = query.count()
        transactions = query.order_by(Transaction.created_at.desc()).offset((page - 1) * page_size).limit(
            page_size).all()

        return {
            "data": transactions,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size) // page_size
        }

    @staticmethod
    def create_transaction(db: Session, transaction: Transaction) -> Transaction:
        try:
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            return transaction
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Transaction creation error: {str(e)}")