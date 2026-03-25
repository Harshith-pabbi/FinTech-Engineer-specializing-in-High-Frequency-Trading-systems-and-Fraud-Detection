from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class TransactionRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    merchant_id: str = Field(..., description="Unique merchant identifier")
    amount: float = Field(..., gt=0, description="Transaction amount")
    currency: str = Field(default="USD", description="Currency code")
    category: str = Field(..., description="Merchant category")
    location: str = Field(..., description="Transaction location")
    user_status: str = Field(default="active", description="User account status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "usr_123",
                "merchant_id": "mer_456",
                "amount": 150.0,
                "currency": "USD",
                "category": "electronics",
                "location": "New York",
                "user_status": "active"
            }
        }
    )

class TransactionResponse(BaseModel):
    transaction_id: str
    status: str
    risk_score: Optional[float] = None
    message: str
