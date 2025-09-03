from decimal import Decimal

from pydantic import BaseModel, field_validator

class BalanceResponse(BaseModel):
    balance: Decimal
    currency: str

class DepositRequest(BaseModel):
    amount: float
    card_number: str
    card_holder: str
    expiry_month: int
    expiry_year: int
    cvv: str

    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0 or v > 10000:
            raise ValueError('Amount must be between 0 and 10000')
        return v

    @field_validator('card_number')
    def validate_card_number(cls, v):
        card_clean = v.replace(" ", "")
        if not card_clean.isdigit() or len(card_clean) != 16:
            raise ValueError('Invalid card number format')
        return card_clean


class WithdrawRequest(BaseModel):
    amount: float
    bank_account: str
    back_account_name: str

    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0 or v > 50000:
            raise ValueError('Amount must be between 0 and 50000')
        return v


class OperationResponse(BaseModel):
    transaction_id: int
    reference_code: str
    status: str
    message: str
    new_balance: str
