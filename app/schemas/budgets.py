from pydantic import BaseModel, Field
from datetime import date

class BudgetUpsertIn(BaseModel):
    category_id: int
    month: date  # ej: "2026-02-01"
    limit_amount: float = Field(..., gt=0)

class BudgetStatusOut(BaseModel):
    category_id: int
    category_name: str
    month: date
    limit_amount: float
    spent: float
    remaining: float
    percent_used: float