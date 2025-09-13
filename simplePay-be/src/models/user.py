from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, Session
from passlib.context import CryptContext
from datetime import datetime

from sqlalchemy.sql import expression

from .base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Questa classe rappresenta un utente del sistema
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
    is_deleted = Column(Boolean, default=False, nullable=False, server_default=expression.false())
    deleted_at = Column(DateTime, default=None, nullable=True)

    wallet = relationship("Wallet", back_populates="user")

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    def authenticate(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

