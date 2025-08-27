from sqlalchemy import Column, Integer, String, DECIMAL, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    from_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)
    to_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)
    transaction_type = Column(String(20), nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    currency = Column(String(3), default="EUR", nullable=False)
    description = Column(Text, nullable=True)
    reference_code = Column(String(100), unique=True, nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    fee_amount = Column(DECIMAL(15, 2), default=0.00, nullable=False)
    created_at = Column(DateTime, nullable=False)
    processed_at = Column(DateTime, nullable=True)

    from_wallet = relationship("Wallet", foreign_keys=[from_wallet_id], back_populates="transactions_from")
    to_wallet = relationship("Wallet", foreign_keys=[to_wallet_id], back_populates="transactions_to")
    transaction_type_rel = relationship("TransactionType", back_populates="transactions")
    notifications = relationship("Notification", back_populates="transaction")