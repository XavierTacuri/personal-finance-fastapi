from datetime import date
from app.schemas.transaction import TransactionType
from app.schemas.report import MonthlyReport
from app.repositories.transactions_repo import TransactionRepository

class ReportService:
    def __init__(self, repo: TransactionRepository)-> None:
        self.repo = repo

    def monthly_report(self,month: str) -> MonthlyReport:
        year , m = month.split('-')
        year = int(year)
        m = int(m)

        start = date(year, m, 1)
        if m == 12:
            end = date(year+1,1,1)
        else:
            end = date(year, m+1,1)

        txs = self.repo.list(date_from=start, date_to=end)

        total_income = sum (t.amount for t in txs if t.type == TransactionType.income)
        total_expense = sum(t.amount for t in txs if t.type == TransactionType.expense)
        savings = total_income - total_expense

        expense_category = {}
        for t in txs:
            if t.type == TransactionType.expense:
                expense_category[t.category] = expense_category.get(t.category, 0.0) + t.amount

        return MonthlyReport(month=month,
                            total_income = round(total_income,2),
                            total_expense= round(total_expense,2),
                            savings = round(savings,2),
                            expenses_category={k: round(v,2) for k, v in expense_category.items()}
                            )


