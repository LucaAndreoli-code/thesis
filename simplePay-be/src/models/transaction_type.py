from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, Text
from sqlalchemy.orm import relationship
from .base import Base


class TransactionType(Base):
    __tablename__ = "transaction_types"

    id = Column(Integer, primary_key=True)
    type_code = Column(String(20), unique=True, nullable=False)
    type_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    fee_percentage = Column(DECIMAL(5, 4), default=0.0000, nullable=False)
    min_amount = Column(DECIMAL(15, 2), nullable=True)
    max_amount = Column(DECIMAL(15, 2), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    transactions = relationship("Transaction", back_populates="transaction_type")