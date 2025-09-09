from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from src.database.database import get_db
from src.models import User
from src.schemas.payments import PaymentResponse, PaymentRequest
from src.service.auth import AuthService
from src.service.transaction import TransactionService

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/send", response_model=PaymentResponse)
def create_payment(
        payment: PaymentRequest,
        db: Session = Depends(get_db),
        current_user:User=Depends(AuthService.get_current_user),
):
    try:
        return TransactionService(db).exchange_money(payment, current_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment error: {str(e)}")


@router.get("/transactions")
def get_transactions(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        search: Optional[str] = Query(None, description="Ricerca per descrizione, codice riferimento o tipo"),
        start_date: Optional[datetime] = Query(None, description="Data di inizio filtro (formato: YYYY-MM-DD)"),
        end_date: Optional[datetime] = Query(None, description="Data di fine filtro (formato: YYYY-MM-DD)"),
        db: Session = Depends(get_db),
        current_user: User = Depends(AuthService.get_current_user)
):
    try:
        return TransactionService(db).get_transactions_paginated(current_user, page, page_size, search, start_date, end_date)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")
