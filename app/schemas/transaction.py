from datetime import date
from enum import Enum
from pydantic import BaseModel,Field

class TransactionType(str,Enum):
    income = "income"
    expense = "expense"

class Category(str, Enum):
    food = "food"
    transport = "transport"
    rent = "rent"
    salary = "salary"
    entertainment = "entertainment"
    education = "education"
    health = "health"
    utilities = "utilities"

class TransactionCreate(BaseModel):
    type: TransactionType
    category: Category
    amount: float = Field( ..., gt=0 )
    date: date
    note: str | None = Field(default=None, max_length=200)

class TransactionOut(TransactionCreate):
    id: int
