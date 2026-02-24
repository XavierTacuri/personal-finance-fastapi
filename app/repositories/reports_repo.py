from datetime import date
from sqlmodel import Session, select
from sqlalchemy import func
from app.models.db_models import Transaction, Category  # ajusta: CategoryBD si es tu nombre

class ReportsRepository:
    def __init__(self, db: Session):
        self.db = db

    def monthly_totals(self, user_id: int, year: int, month: int) -> dict:
        # rango [start, end)
        start = date(year, month, 1)
        if month == 12:
            end = date(year + 1, 1, 1)
        else:
            end = date(year, month + 1, 1)

        stmt = (
            select(Transaction.type, func.coalesce(func.sum(Transaction.amount), 0.0))
            .where(Transaction.user_id == user_id)
            .where(Transaction.txn_date >= start)
            .where(Transaction.txn_date < end)
            .group_by(Transaction.type)
        )
        rows = self.db.exec(stmt).all()
        # rows: [(TransactionType.income, 123.0), (TransactionType.expense, 50.0)]
        out = {t: float(s) for t, s in rows}
        return out

    def totals_by_category(self, user_id: int, year: int, month: int, tx_type):
        start = date(year, month, 1)
        if month == 12:
            end = date(year + 1, 1, 1)
        else:
            end = date(year, month + 1, 1)

        stmt = (
            select(Category.id, Category.name, func.coalesce(func.sum(Transaction.amount), 0.0))
            .join(Transaction, Transaction.category_id == Category.id)
            .where(Transaction.user_id == user_id)
            .where(Transaction.type == tx_type)
            .where(Transaction.txn_date >= start)
            .where(Transaction.txn_date < end)
            .group_by(Category.id, Category.name)
            .order_by(func.sum(Transaction.amount).desc())
        )
        return self.db.exec(stmt).all()

    def daily_totals(self, user_id: int, date_from: date, date_to: date, tx_type):
        # date_to inclusivo -> convertimos a end exclusivo sumando 1 día en el service (más limpio),
        # o lo manejas aquí. Yo lo manejo aquí:
        stmt = (
            select(Transaction.txn_date, func.coalesce(func.sum(Transaction.amount), 0.0))
            .where(Transaction.user_id == user_id)
            .where(Transaction.type == tx_type)
            .where(Transaction.txn_date >= date_from)
            .where(Transaction.txn_date <= date_to)
            .group_by(Transaction.txn_date)
            .order_by(Transaction.txn_date.asc())
        )
        return self.db.exec(stmt).all()