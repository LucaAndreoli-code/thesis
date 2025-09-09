from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, sessionmaker
from src.service.token import TokenService
from src.models.user import User
from src.database.database import get_db, engine
from src.service.user import UserService
from src.schemas.auth import UserLogin, UserResponse, UserRegister

security = HTTPBearer()

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, user_data: UserLogin):
        try:
            # Authenticate user
            user = UserService(self.db).authenticate_user(str(user_data.email), user_data.password)
            access_token = TokenService.generate_token(user)

            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

    def register(self, user_data: UserRegister):
        try:
            user = UserService(self.db).create_user(user_data.model_dump())

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
    ) -> User:
        token = credentials.credentials

        # Verify token and get payload
        payload = TokenService.verify_token(token)
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        # Creao una nuova sessione per trovare l'utente perché get_db non è disponibile qui essendo un metodo statico
        dbSession = sessionmaker(bind=engine)
        db = dbSession()
        user = db.query(User).filter(User.id == user_id).first()
        db.close()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )


        return user