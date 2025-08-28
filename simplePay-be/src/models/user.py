from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config.config import SECRET_KEY
import jwt
import uuid

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    wallet = relationship("Wallet", back_populates="user", uselist=False)

    def generate_jwt(self):
        try:
            payload = {
                "user_id": self.id,
                "username": self.username,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "exp": datetime.utcnow() + timedelta(hours=1),
                "iat": datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return token
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Errore generazione token: {str(e)}")

    def verify_password(self, password: str, db) -> bool:
        try:
            user_db = db.query(User).filter(
                (User.email == self.email)
            ).first()
            # verifica che ci sia l'utente e che la password corrisponda
            if user_db and pwd_context.verify(password, user_db.password_hash):
                return user_db
            raise HTTPException(status_code=400, detail=f"Invalid email or password")
        except Exception as e:
            raise e

    def create_user(self, db):
        from src.models import Wallet
        # Verifica se l'utente esiste già
        existing_user = db.query(User).filter(
            (User.username == self.username) | (User.email == self.email)
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this username or email already exists")
        try:
            db.add(self)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

        # Create wallet
        wallet_number = f"SP{str(uuid.uuid4().int)[:12]}"
        db_wallet = Wallet(
            user_id=self.id,
            wallet_number=wallet_number,
            balance=0.00
        )
        try:
            db.add(db_wallet)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def find_by_email(db, email: str):
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(status_code=404, detail="Utente non trovato")
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Errore ricerca utente: {str(e)}")