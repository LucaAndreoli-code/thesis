from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.user import User
from src.service.auth import AuthService
from src.service.user import UserService

router = APIRouter(prefix="/user", tags=["User"])

@router.delete("/delete")
def delete_user_account(db: Session = Depends(get_db),
        current_user:User=Depends(AuthService.get_current_user)):
    try:
        UserService(db).delete_by_id(current_user.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User delete error: {str(e)}")