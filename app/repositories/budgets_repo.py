from datetime import date
from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy import func

from app.models.db_models import Budget, Category, Transaction, TransactionType


class BudgetsRepository:
    def __init__(self, db: Session):
        self.db = db

    def _validate_category_for_user(self, user_id: int, category_id: int) -> None:
        row = self.db.exec(
            select(Category.id).where(
                Category.id == category_id,
                Category.user_id == user_id,
                Category.is_active == True,
            )
        ).first()
        if not row:
            raise HTTPException(status_code=404, detail="Category not found for this user")

    def upsert(self, user_id: int, category_id: int, month: date, limit_amount: float) -> Budget:
        self._validate_category_for_user(user_id, category_id)

        b = self.db.exec(
            select(Budget).where(
                Budget.user_id == user_id,
                Budget.category_id == category_id,
                Budget.month == month,
            )
        ).first()

        if b:
            b.limit_amount = limit_amount
        else:
            b = Budget(
                user_id=user_id,
                category_id=category_id,
                month=month,
                limit_amount=limit_amount,
            )
            self.db.add(b)

        self.db.commit()
        self.db.refresh(b)
        return b

    def list_for_month(self, user_id: int, month: date):
        # trae budgets + nombre de categoría
        stmt = (
            select(Budget.category_id, Category.name, Budget.month, Budget.limit_amount)
            .join(Category, Budget.category_id == Category.id)
            .where(Budget.user_id == user_id)
            .where(Budget.month == month)
            .order_by(Category.name.asc())
        )
        budgets = self.db.exec(stmt).all()

        # gasto real (solo expenses) del mes del budget:
        # asumimos que Transaction.txn_date es date, y queremos rango [month, next_month)
        # calculamos next_month
        if month.month == 12:
            next_month = date(month.year + 1, 1, 1)
        else:
            next_month = date(month.year, month.month + 1, 1)

        spent_stmt = (
            select(Transaction.category_id, func.coalesce(func.sum(Transaction.amount), 0.0))
            .where(Transaction.user_id == user_id)
            .where(Transaction.type == TransactionType.expense)
            .where(Transaction.txn_date >= month)
            .where(Transaction.txn_date < next_month)
            .group_by(Transaction.category_id)
        )
        spent_rows = self.db.exec(spent_stmt).all()
        spent_map = {cid: float(total) for cid, total in spent_rows}

        return budgets, spent_map