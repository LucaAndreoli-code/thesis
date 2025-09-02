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
    reference_code_from = f"PAY{uuid.uuid4().hex[:8].upper()}"

    try:
        # Create transaction
        transaction_user_from = Transaction(
            from_wallet_id=from_wallet.id,
            to_wallet_id=to_wallet.id,
            amount=payment_amount,
            description=payment.description or f"Payment to {to_wallet.wallet_number}",
            reference_code=reference_code_from,
            status="completed",
            transaction_type="send"
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
        db.commit()
        db.refresh(transaction_user_from)

        reference_code_to = f"PAY{uuid.uuid4().hex[:8].upper()}"

        transaction_user_to = Transaction(
            from_wallet_id=to_wallet.id,
            to_wallet_id=from_wallet.id,
            amount=payment_amount,
            description=payment.description or f"Receiving from {from_wallet.wallet_number}",
            reference_code=reference_code_to,
            parent_reference_code=reference_code_from,
            status="completed",
            transaction_type="receive"
        )

        # Save to database
        db.add(transaction_user_to)
        db.commit()
        db.refresh(transaction_user_to)

        return PaymentResponse(
            reference_code=reference_code_from,
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
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Get user's wallet
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()

    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # Query for user's transactions
    offset = (page - 1) * limit

    transactions = db.query(Transaction).filter(
        or_(
            Transaction.from_wallet_id == wallet.id,
            Transaction.to_wallet_id == wallet.id
        )
    ).order_by(Transaction.created_at.desc()).offset(offset).limit(limit).all()

    # Count total for pagination
    total = db.query(Transaction).filter(
        or_(
            Transaction.from_wallet_id == wallet.id,
            Transaction.to_wallet_id == wallet.id
        )
    ).count()

    # Format transactions based on type and user perspective
    formatted_transactions = []
    processed_references = set()

    for tx in transactions:
        # Skip if already processed
        if tx.reference_code in processed_references:
            continue

        # Determina il tipo di transazione dal punto di vista dell'utente
        if tx.transaction_type == "deposit":
            transaction_type = "deposit"
        elif tx.transaction_type == "withdraw":
            transaction_type = "withdraw"
        elif tx.from_wallet_id == wallet.id and tx.to_wallet_id != wallet.id:
            # L'utente ha inviato soldi
            transaction_type = "send"
        elif tx.to_wallet_id == wallet.id and tx.from_wallet_id != wallet.id:
            # L'utente ha ricevuto soldi
            transaction_type = "receive"
        else:
            continue  # Skip transazioni anomale

        formatted_transactions.append({
            "id": tx.id,
            "type": transaction_type,
            "amount": abs(tx.amount),  # Sempre positivo, il tipo indica la direzione
            "currency": tx.currency,
            "description": tx.description,
            "reference_code": tx.reference_code,
            "status": tx.status,
            "created_at": tx.created_at,
            "processed_at": tx.processed_at
        })

        # Marca il reference_code come processato
        processed_references.add(tx.reference_code)

    return {
        "transactions": formatted_transactions,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": len(formatted_transactions),  # Usa il count dei risultati filtrati
            "total_pages": (len(formatted_transactions) + limit) // limit
        }
    }