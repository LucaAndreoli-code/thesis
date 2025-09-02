from operator import and_

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from decimal import Decimal
from datetime import datetime
import uuid
from typing import Optional
from src.database.database import get_db  # Your database session dependency
from src.models import User
from src.models.wallet import Wallet
from src.models.transaction import Transaction
from src.service.auth import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

class PaymentRequest(BaseModel):
    to_user_email: str
    amount: float
    description: Optional[str] = None

    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v


class PaymentResponse(BaseModel):
    reference_code: str
    status: str
    message: str


@router.post("/send", response_model=PaymentResponse)
async def create_payment(
        payment: PaymentRequest,
        current_user:User=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Get wallets
    from_wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    to_wallet = db.query(Wallet).join(User, Wallet.user_id == User.id).filter(
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
            description=payment.description or f"Payment to {to_wallet.wallet_number}",
            reference_code=reference_code,
            status="completed",
            transaction_type="send"
        )

        transaction_user_to = Transaction(
            from_wallet_id=to_wallet.id,
            to_wallet_id=from_wallet.id,
            amount=payment_amount,
            description=payment.description or f"Receiving from {from_wallet.wallet_number}",
            reference_code=reference_code,
            status="completed",
            transaction_type="receive"
        )

        # Update balances
        from_wallet.balance -= payment_amount
        to_wallet.balance += payment_amount
        from_wallet.updated_at = datetime.utcnow()
        to_wallet.updated_at = datetime.utcnow()

        # Set processed timestamp
        transaction_user_from.processed_at = datetime.utcnow()

        # Save to database
        db.add(transaction_user_from)
        db.add(transaction_user_to)
        db.commit()
        db.refresh(transaction_user_to)
        db.refresh(transaction_user_from)

        return PaymentResponse(
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


@router.get("/transactions")
async def get_transactions(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        search: Optional[str] = Query(None, description="Ricerca per descrizione, codice riferimento o tipo"),
        start_date: Optional[datetime] = Query(None, description="Data di inizio filtro (formato: YYYY-MM-DD)"),
        end_date: Optional[datetime] = Query(None, description="Data di fine filtro (formato: YYYY-MM-DD)"),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Get user's wallet
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()

    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    query = db.query(Transaction).filter(
        or_(
            # Caso 1: from_wallet_id = wallet.id AND transaction_type = 'send'
            and_(Transaction.from_wallet_id == wallet.id, Transaction.transaction_type == "send"),
            # Caso 2: from_wallet_id = wallet.id AND transaction_type = 'receive'
            and_(Transaction.from_wallet_id == wallet.id, Transaction.transaction_type == "receive"),
            # Caso 3: to_wallet_id = wallet.id AND from_wallet_id IS NULL AND transaction_type = 'deposit'
            and_(Transaction.to_wallet_id == wallet.id,
                 and_(Transaction.from_wallet_id.is_(None), Transaction.transaction_type == "deposit")),
            # Caso 4: from_wallet_id = wallet.id AND to_wallet_id IS NULL AND transaction_type = 'withdraw'
            and_(Transaction.from_wallet_id == wallet.id,
                 and_(Transaction.to_wallet_id.is_(None), Transaction.transaction_type == "withdraw"))
        )
    )

    # Applica filtro di ricerca se fornito
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Transaction.description.ilike(search_term),
                Transaction.reference_code.ilike(search_term),
                Transaction.transaction_type.ilike(search_term)
            )
        )

    # Applica filtri per data se forniti
    if start_date:
        query = query.filter(Transaction.created_at >= start_date)
    if end_date:
        query = query.filter(Transaction.created_at <= end_date)

    total = query.count()
    transactions = query.order_by(Transaction.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {
        "data": transactions,
        "page": page,
        "page_size": page_size,
        "total": total,  # Usa il count dei risultati filtrati
        "total_pages": (total + page_size) // page_size
    }