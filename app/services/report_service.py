from datetime import date
from os import name

from sqlalchemy.engine import row

from app.schemas import category
from app.schemas.report import MonthlySummaryOut, CategoryTotalOut, DailyTotalOut
from app.models.db_models import TransactionType
from app.repositories.reports_repo import ReportsRepository



class ReportService:
    def __init__(self, repo:ReportsRepository):
        self.repo = repo

    def monthly_summary(self,user_id:int,year:int,month:int)->MonthlySummaryOut:

        total=self.repo.monthly_totals(user_id=user_id,year=year,month=month)
        income=float(total.get(TransactionType.income,0.0))
        expense=float(total.get(TransactionType.expense,0.0))

        return MonthlySummaryOut(
                year=year,
                month=month,
                income=income,
                expense=expense,
                net = income - expense,
                )
    def by_category(self,user_id:int,year:int,month:int,tx_type:TransactionType):
        rows=self.repo.totals_by_category(user_id=user_id,year=year,month=month,tx_type=tx_type)
        return [
            CategoryTotalOut(category_id = category_id,
                             category_name = category_name,
                             total = float(total),)
            for category_id,category_name,total in rows
            ]

    def daily(self,user_id:int,date_from:date,date_to:date,tx_type:TransactionType):
        rows = self.repo.daily_totals(user_id=user_id,date_from=date_from,date_to=date_to,tx_type=tx_type)
        return [DailyTotalOut(day=d, total=float(t)) for d, t in rows]