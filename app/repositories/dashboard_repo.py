from datetime import date
from sqlmodel import Session, select
from sqlalchemy import func

from app.models.db_models import Transaction, Category, TransactionType, Budget


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def _month_range(self, month: date) -> tuple[date, date]:
        m = month.replace(day=1)
        if m.month == 12:
            end = date(m.year + 1, 1, 1)
        else:
            end = date(m.year, m.month + 1, 1)
        return m, end

    def monthly_totals(self, user_id: int, month: date):
        start, end = self._month_range(month)
        stmt = (
            select(Transaction.type, func.coalesce(func.sum(Transaction.amount), 0.0))
            .where(Transaction.user_id == user_id)
            .where(Transaction.txn_date >= start)
            .where(Transaction.txn_date < end)
            .group_by(Transaction.type)
        )
        return self.db.exec(stmt).all()

    def top_by_category(self, user_id: int, month: date, tx_type: TransactionType, limit: int = 5):
        start, end = self._month_range(month)
        stmt = (
            select(Category.id, Category.name, func.coalesce(func.sum(Transaction.amount), 0.0))
            .join(Transaction, Transaction.category_id == Category.id)
            .where(Transaction.user_id == user_id)
            .where(Transaction.type == tx_type)
            .where(Transaction.txn_date >= start)
            .where(Transaction.txn_date < end)
            .group_by(Category.id, Category.name)
            .order_by(func.sum(Transaction.amount).desc())
            .limit(limit)
        )
        return self.db.exec(stmt).all()

    def recent_transactions(self, user_id: int, limit: int = 10):
        stmt = (
            select(Transaction, Category.name)
            .join(Category, Transaction.category_id == Category.id)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.txn_date.desc(), Transaction.id.desc())
            .limit(limit)
        )
        return self.db.exec(stmt).all()

    def budgets_status(self, user_id: int, month: date):
        start, end = self._month_range(month)

        # budgets del mes + nombre categoría
        bstmt = (
            select(Budget.category_id, Category.name, Budget.month, Budget.limit_amount)
            .join(Category, Budget.category_id == Category.id)
            .where(Budget.user_id == user_id)
            .where(Budget.month == start)
            .order_by(Category.name.asc())
        )
        budgets = self.db.exec(bstmt).all()

        # gastos reales del mes por categoría (expense)
        sstmt = (
            select(Transaction.category_id, func.coalesce(func.sum(Transaction.amount), 0.0))
            .where(Transaction.user_id == user_id)
            .where(Transaction.type == TransactionType.expense)
            .where(Transaction.txn_date >= start)
            .where(Transaction.txn_date < end)
            .group_by(Transaction.category_id)
        )
        spent = {cid: float(total) for cid, total in self.db.exec(sstmt).all()}

        return budgets, spent