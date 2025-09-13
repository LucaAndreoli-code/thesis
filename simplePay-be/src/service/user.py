import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.user import User
from src.models.wallet import Wallet
from src.service.wallet import WalletService

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: dict) -> User:
        # Check if user already exists
        existing_user = self.db.query(User).filter(
            (User.username == user_data.get('username')) |
            (User.email == user_data.get('email'))
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User with this username or email already exists"
            )


        if len(user_data['password']) < 8:
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters long"
            )

        try:
            # Hash password and create user
            hashed_password = User.hash_password(user_data['password'])
            db_user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=hashed_password,
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
            )

            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)

            # Create default wallet
            WalletService(self.db).create_wallet(db_user.id)

            return db_user

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"User creation error: {str(e)}")

    def authenticate_user(self, email: str, password: str) -> User:
        user = UserService(self.db).get_user_by_email(email)

        if not user or not user.authenticate(password) or user.is_deleted:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.db.query(User).filter(User.email == email and User.is_deleted == False).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    # anonimizza l'utente invece di eliminarlo per mantenere l'integrità referenziale
    def delete_by_id(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        user.username = f"deleted_user_{user_id}"
        user.first_name = "Deleted"
        user.last_name = "User"
        user.email = f"deleted_{user_id}@example.com"
        user.is_deleted = True
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"User deletion error: {str(e)}")

    # per testing
    def delete_by_email(self, email: str):
        wallet = self.db.query(Wallet).filter(Wallet.user.has(email=email)).first()
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            self.db.delete(wallet)
            self.db.delete(user)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"User deletion error: {str(e)}")