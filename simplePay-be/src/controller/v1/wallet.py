from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.user import User
from src.schemas.wallet import OperationResponse, DepositRequest, WithdrawRequest, BalanceResponse
from src.service.auth import AuthService
from src.service.wallet import WalletService

router = APIRouter(prefix="/wallet", tags=["Wallet"])

@router.post("/deposit", response_model=OperationResponse)
def deposit_to_wallet(
        deposit: DepositRequest,
        current_user: User = Depends(AuthService.get_current_user),
        db: Session = Depends(get_db)
):
    try:
        return WalletService(db).deposit_to_wallet(deposit, current_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deposit error: {str(e)}")


@router.post("/withdraw", response_model=OperationResponse)
def withdraw_from_wallet(
        withdraw: WithdrawRequest,
        current_user: User = Depends(AuthService.get_current_user),
        db: Session = Depends(get_db)
):
    try:
        return WalletService(db).withdraw_from_wallet(withdraw, current_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Withdrawal error: {str(e)}")


@router.get("/balance", response_model=BalanceResponse)
def get_wallet_balance(
        current_user: User = Depends(AuthService.get_current_user),
        db: Session = Depends(get_db)
) -> BalanceResponse:
    try:
        user_wallet = WalletService(db).get_user_wallet(current_user)
        return user_wallet.get_balance()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Balance retrieval error: {str(e)}")