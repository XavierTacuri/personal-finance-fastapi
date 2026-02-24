from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class MonthlySummaryOut(BaseModel):
    year: int
    month: int
    income: float
    expense: float
    net: float

class CategoryTotalOut(BaseModel):
    category_id: int
    category_name: str
    total: float

class DailyTotalOut(BaseModel):
    day: date
    total: float