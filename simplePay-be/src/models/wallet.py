from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wallet_number = Column(String(20), unique=True, nullable=False, index=True)
    balance = Column(DECIMAL(15, 2), default=0.00)
    currency = Column(String(3), default="EUR")
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="wallet")
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.from_wallet_id",
                                     back_populates="from_wallet")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.to_wallet_id",
                                         back_populates="to_wallet")