from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from app.models.db_models import TransactionType

class DashboardSummary(BaseModel):
    month: date
    income: float
    expense: float
    net: float

class DashboardCategorySlice(BaseModel):
    category_id: int
    category_name: str
    total: float
    type: TransactionType  # income|expense

class DashboardTransactionItem(BaseModel):
    id: int
    category_id: int
    category_name: str
    type: TransactionType
    amount: float
    currency: str
    txn_date: date
    note: Optional[str] = None

class DashboardBudgetItem(BaseModel):
    category_id: int
    category_name: str
    month: date
    limit_amount: float
    spent: float
    remaining: float
    percent_used: float

class DashboardOut(BaseModel):
    summary: DashboardSummary
    top_expenses_by_category: List[DashboardCategorySlice]
    top_incomes_by_category: List[DashboardCategorySlice]
    budgets: List[DashboardBudgetItem]
    recent_transactions: List[DashboardTransactionItem]