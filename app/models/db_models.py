from __future__ import annotations

from datetime import datetime,date
from enum import Enum
from operator import index
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Index




class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    name_user: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: str = Field (nullable=False,index=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    categories: List["Category"] = Relationship(back_populates="user")
    transactions: List["Transaction"] = Relationship(back_populates="user")
    budgets: List["Budget"] = Relationship(back_populates="user")

    __table_args__ = (UniqueConstraint("email",name="uq_user_email"),)

class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    name: str = Field(nullable=False, max_length=50)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: Optional[User] = Relationship(back_populates="categories")
    transactions: List["Transaction"] = Relationship(back_populates="category")
    budgets: List["Budget"] = Relationship(back_populates="category")

    __table_args__ = (
        UniqueConstraint("user_id",name="uq_category_user_name"),
        Index("ix_categories_user_name", "user_id", "name"),
    )

class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    category_id: int = Field(foreign_key="categories.id", nullable=False, index=True)

    type: TransactionType = Field(nullable=False)
    amount: float = Field(nullable=False)
    currency: str = Field(default="USD",max_length=3, nullable=False)

    txn_date: date = Field(nullable=False,index=True)
    note: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: Optional[User] = Relationship(back_populates="transactions")
    category: Optional[Category] = Relationship(back_populates="transactions")

    __table_args__ = (
        Index("ix_transactions_user_date","user_id","txn_date"),
        Index("ix_transactions_user_type","user_id","type"),
        )
class Budget(SQLModel, table=True):
    __tablename__ = "budgets"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    category_id: int = Field(foreign_key="categories.id", nullable=False, index=True)

    month: date = Field(nullable=False,index=True)
    limit_amount: float = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: Optional[User] = Relationship(back_populates="budgets")
    category: Optional[Category] = Relationship(back_populates="budgets")

    __table_args__ = (
        UniqueConstraint("user_id","category_id","month",name="uq_budget_user_category_month"),
        Index("ix_budgets_user_month","user_id","month"),
        )





