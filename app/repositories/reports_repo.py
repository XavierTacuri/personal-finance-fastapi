from sqlmodel import Session, select
from datetime import date
from sqlalchemy import func
from app.models.db_models import Transaction,Category,TransactionType

class ReportsRepository:
    def __init__(self,db:Session):
        self.db = db

    def monthly_total(self,user_id:int,year:int,month:int):
        start=date(year,month,1)

        if month == 12:
            end = date(year+1,1,1)
        else:
            end = date(year,month+1,1)

        stmt= (select(
            Transaction.type,
            func.coalesce(func.sum(Transaction.amount),0.0)
            )
            .where(Transaction.user_id == user_id)
            .where(Transaction.txn_date >= start)
            .where(Transaction.txn_date < end)
            .group_by(Transaction.type)
        )
        rows = self.db.exec(stmt).all()
        total={t: float(s) for t ,s in rows}
        return total,start,end

    def expenses_by_category(self,user_id:int,start:date,end: date):
        stmt= (
            select(
                Category.id,
                Category.name,
                func.coalesce(func.sum(Transaction.amount),0.0)
            )
            .join(Category,Transaction.category_id == Category.id)
            .where(Transaction.user_id == user_id)
            .where(Transaction.type==TransactionType.expense)
            .where(Transaction.txn_date >= start)
            .where(Transaction.txn_date < end)
            .group_by(Category.id,Category.name)
            .order_by(func.sum(Transaction.amount).desc())
        )
        return self.db.exec(stmt).all()
