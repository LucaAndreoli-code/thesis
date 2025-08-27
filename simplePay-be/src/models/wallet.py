from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wallet_number = Column(String(50), unique=True, nullable=False)
    wallet_type = Column(String(20), nullable=False)
    balance = Column(DECIMAL(15, 2), default=0.00, nullable=False)
    available_balance = Column(DECIMAL(15, 2), default=0.00, nullable=False)
    status = Column(String(20), default="active", nullable=False)
    currency = Column(String(3), default="EUR", nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="wallets")
    wallet_type_rel = relationship("WalletType", back_populates="wallets")
    transactions_from = relationship("Transaction", foreign_keys="Transaction.from_wallet_id", back_populates="from_wallet")
    transactions_to = relationship("Transaction", foreign_keys="Transaction.to_wallet_id", back_populates="to_wallet")