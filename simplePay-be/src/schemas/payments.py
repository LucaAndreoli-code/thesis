from typing import Optional
from pydantic import BaseModel, field_validator

class PaymentRequest(BaseModel):
    to_user_email: str
    amount: float
    description: Optional[str] = None

    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v


class PaymentResponse(BaseModel):
    reference_code: str
    status: str
    message: str