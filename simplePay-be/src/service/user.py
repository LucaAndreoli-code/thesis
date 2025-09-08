import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.user import User
from src.models.wallet import Wallet
from .wallet import WalletService


class UserService:
    @staticmethod
    def create_user(db: Session, user_data: dict) -> User:
        # Check if user already exists
        existing_user = db.query(User).filter(
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

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            # Create default wallet
            WalletService.create_wallet(db, db_user.id)

            return db_user

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"User creation error: {str(e)}")

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        user = UserService.get_user_by_email(db, email)

        if not user or not user.authenticate(password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def delete_by_id(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            db.delete(user)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"User deletion error: {str(e)}")

    @staticmethod
    def delete_by_email(db: Session, email: str):
        wallet = db.query(Wallet).filter(Wallet.user.has(email=email)).first()
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            db.delete(wallet)
            db.delete(user)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"User deletion error: {str(e)}")