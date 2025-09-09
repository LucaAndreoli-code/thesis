from decimal import Decimal
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from .base import Base
from ..schemas.wallet import BalanceResponse

# Questa classe rappresenta un portafoglio digitale associato a un utente
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

    def get_balance(self) -> BalanceResponse:
        return BalanceResponse(balance=Decimal(self.balance), currency=str(self.currency))

    def deposit(self, amount: Decimal):
        self.balance += amount
        self.updated_at = datetime.utcnow()

    def withdraw(self, amount: Decimal):
        self.balance -= amount
        self.updated_at = datetime.utcnow()