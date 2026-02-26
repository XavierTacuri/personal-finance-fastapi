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

    def by_category(self, user_id: int, year: int, month: int, tx_type: TransactionType):
        start = date(year, month, 1)
        end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)

        rows = self.repo.totals_by_category(user_id=user_id, start=start, end=end, tx_type=tx_type)

        grand_total = sum(float(total) for _, _, total in rows) or 0.0

        out = []
        for category_id, category_name, total in rows:
            total_f = float(total)
            percent = (total_f / grand_total * 100.0) if grand_total > 0 else 0.0
            out.append(CategoryTotalOut(
                category_id=category_id,
                category_name=category_name,
                total=total_f,
                percent=percent,
            ))
        return out