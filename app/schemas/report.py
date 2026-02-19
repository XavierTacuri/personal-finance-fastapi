from pydantic import BaseModel
from typing import List


class categorySpend(BaseModel):
    category_id: int
    category_name: str
    total: float

class monthlyReport(BaseModel):
    user_id: int
    month: str
    total_income: float
    total_expense: float
    balance: float
    expense_by_category: List[categorySpend]
