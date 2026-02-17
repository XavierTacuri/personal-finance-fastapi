from datetime import date
from pydantic import BaseModel, Field
from app.models.db_models import TransactionType


class TransactionCreate(BaseModel):
    user_id: int
    category_id: int
    type: TransactionType
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=3)
    txn_date: date
    note: str | None = Field(default=None, max_length=200)


class TransactionOut(TransactionCreate):
    id: int
    category_name: str | None = None
