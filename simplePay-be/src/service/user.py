import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.user import User
from src.models.wallet import Wallet


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
            UserService._create_default_wallet(db, db_user.id)

            return db_user

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"User creation error: {str(e)}")

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        user = UserService.get_user_by_email(db, email)

        if not user or not user.verify_password(password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def update_user(db: Session, user_id: int, update_data: dict) -> User:
        user = UserService.get_user_by_id(db, user_id)

        try:
            for key, value in update_data.items():
                if hasattr(user, key) and key != 'id':
                    setattr(user, key, value)

            db.commit()
            db.refresh(user)
            return user

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"User update error: {str(e)}")

    @staticmethod
    def _create_default_wallet(db: Session, user_id: int):
        wallet_number = f"SP{str(uuid.uuid4().int)[:12]}"
        db_wallet = Wallet(
            user_id=user_id,
            wallet_number=wallet_number,
            balance=0.00,
            status="active",
            currency="EUR"
        )

        try:
            db.add(db_wallet)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Wallet creation error: {str(e)}")