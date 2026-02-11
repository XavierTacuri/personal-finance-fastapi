from pydantic import BaseModel
from typing import Dict
from app.schemas.transaction import Category

class MonthlyReport(BaseModel):
    month : str
    total_income : float
    total_expense : float
    savings : float
    expenses_category: Dict[Category, float]

