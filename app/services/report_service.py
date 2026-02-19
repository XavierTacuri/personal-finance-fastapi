from app.models.db_models import TransactionType


class ReportService:
    def __init__(self, repo):
        self.repo = repo

    def monthly_report(self,user_id:int,year:int,month:int):
        total,start, end = self.repo.monthly_total(user_id,year,month)

        total_income = total.get(TransactionType.income,0.0)
        total_expense = total.get(TransactionType.expense,0.0)
        balance = total_income - total_expense

        cat_rows = self.repo.expenses_by_category(user_id,start,end)
        expense_category = [
            {"category_id": cid, "category_name": name , "total":float(total)}
            for cid, name, total in cat_rows
        ]
        return {
            "user_id": user_id,
            "month": f"{year:04d}-{month:02d}",
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "expense_by_category": expense_category,
        }