# app/repositories/transactions_repo.py

from sqlmodel import Session, select
from app.models.db_models import Transaction, Category


class TransactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, payload):
        tx = Transaction(**payload.model_dump())
        self.db.add(tx)
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def get_all(self, user_id: int):
        statement = (
            select(Transaction, Category.name)
            .join(Category, Transaction.category_id == Category.id)
            .where(Transaction.user_id == user_id)
        )

        results = self.db.exec(statement).all()

        return [
            {
                **tx.model_dump(),
                "category_name": category_name
            }
            for tx, category_name in results
        ]
