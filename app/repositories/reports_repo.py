from datetime import date
from sqlmodel import Session, select
from sqlalchemy import func
from app.models.db_models import Transaction, Category, TransactionType  # ajusta: CategoryBD si es tu nombre

class ReportsRepository:
    def __init__(self, db: Session):
        self.db = db


    def totals_by_category(self, user_id: int, start: date, end: date, tx_type: TransactionType):
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