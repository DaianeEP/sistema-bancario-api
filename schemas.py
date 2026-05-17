from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    username: str
    balance: float

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TransactionCreate(BaseModel):
    type: Literal["DEPOSIT", "WITHDRAW"]
    amount: float = Field(..., gt=0, description="O valor deve ser maior que zero")

class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: float
    timestamp: datetime

    class Config:
        from_attributes = True

class StatementResponse(BaseModel):
    balance: float
    transactions: list[TransactionResponse]
