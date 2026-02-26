# app/repositories/transactions_repo.py
from __future__ import annotations
from datetime import date
from typing import Optional,List

from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy import func
from unicodedata import category

from app.models.db_models import Transaction, Category
from app.schemas.transaction import TransactionCreate,TransactionType,TransactionOut


class TransactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def _validate_category_id_for_user(self, user_id: int, category_id: int) -> None:
        stmt = (
            select(Category.id)
            .where(Category.user_id == user_id)
            .where(Category.id == category_id)
            .where(Category.is_active == True)
        )
        row = self.db.exec(stmt).first()
        if not row:
            raise HTTPException(status_code=404, detail="Category does not exist for this user")

    def create(self, user_id:int,payload:TransactionCreate)->Transaction:
        self._validate_category_id_for_user(user_id,payload.category_id)
        tx = Transaction(
            user_id=user_id,
            category_id=payload.category_id,
            type=payload.type,
            amount=payload.amount,
            currency=payload.currency,
            txn_date=payload.txn_date,
            note=payload.note,
        )
        self.db.add(tx)
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def get_all(self, user_id: int,
                tx_type:Optional[TransactionType]=None,
                category_id: int | None = None,
                date_from:date=None,
                date_to:date=None)->List[TransactionOut]:
        stmt = (
            select(Transaction, Category.name)
            .join(Category, Transaction.category_id == Category.id)
            .where(Transaction.user_id == user_id)
        )

        if tx_type is not None:
            stmt = stmt.where(Transaction.type==tx_type)
        if category_id is not None:
            stmt = stmt.where(Transaction.category_id == category_id)
        if date_from is not None:
            stmt = stmt.where(Transaction.txn_date>=date_from)
        if date_to is not None:
            stmt = stmt.where(Transaction.txn_date<=date_to)

        rows = self.db.exec(stmt).all()

        return [
            TransactionOut(
                id=tx.id,
                category_id=tx.category_id,
                type=tx.type,
                amount=tx.amount,
                currency=tx.currency,
                txn_date=tx.txn_date,
                note=tx.note,
                category_name=cat_name,
            )
            for tx, cat_name in rows
        ]

    def list_page(
            self,
            user_id: int,
            tx_type: TransactionType | None = None,
            category_id: int | None = None,
            date_from: date | None = None,
            date_to: date | None = None,
            sort: str = "desc",  # "asc" | "desc"
            limit: int = 50,
            offset: int = 0,
    ) -> tuple[list[TransactionOut], int]:

        # base query (items) con JOIN para category_name
        stmt = (
            select(Transaction, Category.name)
            .join(Category, Transaction.category_id == Category.id)
            .where(Transaction.user_id == user_id)
        )

        # filtros
        if tx_type is not None:
            stmt = stmt.where(Transaction.type == tx_type)
        if category_id is not None:
            stmt = stmt.where(Transaction.category_id == category_id)
        if date_from is not None:
            stmt = stmt.where(Transaction.txn_date >= date_from)
        if date_to is not None:
            stmt = stmt.where(Transaction.txn_date <= date_to)

        # total count (sin JOIN, más rápido)
        count_stmt = select(func.count()).select_from(Transaction).where(Transaction.user_id == user_id)
        if tx_type is not None:
            count_stmt = count_stmt.where(Transaction.type == tx_type)
        if category_id is not None:
            count_stmt = count_stmt.where(Transaction.category_id == category_id)
        if date_from is not None:
            count_stmt = count_stmt.where(Transaction.txn_date >= date_from)
        if date_to is not None:
            count_stmt = count_stmt.where(Transaction.txn_date <= date_to)

        total = int(self.db.exec(count_stmt).one())

        # sort estable
        if sort == "asc":
            stmt = stmt.order_by(Transaction.txn_date.asc(), Transaction.id.asc())
        else:
            stmt = stmt.order_by(Transaction.txn_date.desc(), Transaction.id.desc())

        # paginación
        stmt = stmt.limit(limit).offset(offset)

        rows = self.db.exec(stmt).all()

        items = [
            TransactionOut(
                id=tx.id,
                category_id=tx.category_id,
                type=tx.type,
                amount=tx.amount,
                currency=tx.currency,
                txn_date=tx.txn_date,
                note=tx.note,
                category_name=cat_name,
            )
            for tx, cat_name in rows
        ]
        return items, total