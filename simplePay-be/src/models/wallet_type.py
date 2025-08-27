from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, Text
from sqlalchemy.orm import relationship
from .base import Base


class WalletType(Base):
    __tablename__ = "wallet_types"

    id = Column(Integer, primary_key=True)
    type_code = Column(String(20), unique=True, nullable=False)
    type_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    daily_limit = Column(DECIMAL(15, 2), nullable=True)
    monthly_limit = Column(DECIMAL(15, 2), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    wallets = relationship("Wallet", back_populates="wallet_type")