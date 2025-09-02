from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    from_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)
    to_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)
    amount = Column(DECIMAL(15, 2), nullable=False)
    currency = Column(String(3), default="EUR")
    description = Column(String(255))
    reference_code = Column(String(50), unique=False, nullable=False, index=True)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    transaction_type = Column(String(20), nullable=True)

    from_wallet = relationship("Wallet", foreign_keys=[from_wallet_id], back_populates="sent_transactions")
    to_wallet = relationship("Wallet", foreign_keys=[to_wallet_id], back_populates="received_transactions")