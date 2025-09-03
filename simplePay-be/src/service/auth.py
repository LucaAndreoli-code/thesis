from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.service.jwt import JWTService
from src.models.user import User
from src.database.database import get_db
from src.service.user import UserService
from src.schemas.auth import UserLogin, UserResponse, UserRegister

security = HTTPBearer()

class AuthService:
    @staticmethod
    def login(user_data: UserLogin, db: Session = Depends(get_db)):
        try:
            # Authenticate user
            user = UserService.authenticate_user(db, str(user_data.email), user_data.password)
            access_token = JWTService.generate_token(user)

            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

    @staticmethod
    def register(user_data: UserRegister, db: Session = Depends(get_db)):
        try:
            user = UserService.create_user(db, user_data.model_dump())

            return UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")

    @staticmethod
    def get_current_user(
            credentials: HTTPAuthorizationCredentials = Depends(security),
            db: Session = Depends(get_db)
    ) -> User:
        token = credentials.credentials

        # Verify token and get payload
        payload = JWTService.verify_token(token)
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user