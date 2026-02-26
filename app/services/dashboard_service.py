from datetime import date
from app.models.db_models import TransactionType
from app.schemas.dashboard import (
    DashboardOut, DashboardSummary, DashboardCategorySlice,
    DashboardTransactionItem, DashboardBudgetItem
)
from app.repositories.dashboard_repo import DashboardRepository


class DashboardService:
    def __init__(self, repo: DashboardRepository):
        self.repo = repo

    def get_dashboard(self, user_id: int, month: date, top_n: int = 5, recent_n: int = 10) -> DashboardOut:
        month = month.replace(day=1)

        # summary
        rows = self.repo.monthly_totals(user_id=user_id, month=month)
        totals = {t: float(s) for t, s in rows}
        income = totals.get(TransactionType.income, 0.0)
        expense = totals.get(TransactionType.expense, 0.0)

        summary = DashboardSummary(
            month=month,
            income=income,
            expense=expense,
            net=income - expense,
        )

        # top categories
        top_exp = self.repo.top_by_category(user_id, month, TransactionType.expense, limit=top_n)
        top_inc = self.repo.top_by_category(user_id, month, TransactionType.income, limit=top_n)

        top_expenses = [
            DashboardCategorySlice(category_id=cid, category_name=name, total=float(total), type=TransactionType.expense)
            for cid, name, total in top_exp
        ]
        top_incomes = [
            DashboardCategorySlice(category_id=cid, category_name=name, total=float(total), type=TransactionType.income)
            for cid, name, total in top_inc
        ]

        # budgets
        budgets_rows, spent_map = self.repo.budgets_status(user_id=user_id, month=month)
        budgets = []
        for cid, cname, m, limit_amount in budgets_rows:
            limit_f = float(limit_amount)
            spent = float(spent_map.get(cid, 0.0))
            remaining = round(limit_f - spent, 2)
            percent_used = round((spent / limit_f * 100.0), 2) if limit_f > 0 else 0.0
            budgets.append(DashboardBudgetItem(
                category_id=cid,
                category_name=cname,
                month=m,
                limit_amount=limit_f,
                spent=spent,
                remaining=remaining,
                percent_used=percent_used,
            ))

        # recent transactions
        recent_rows = self.repo.recent_transactions(user_id=user_id, limit=recent_n)
        recent = [
            DashboardTransactionItem(
                id=tx.id,
                category_id=tx.category_id,
                category_name=cname,
                type=tx.type,
                amount=tx.amount,
                currency=tx.currency,
                txn_date=tx.txn_date,
                note=tx.note,
            )
            for tx, cname in recent_rows
        ]

        return DashboardOut(
            summary=summary,
            top_expenses_by_category=top_expenses,
            top_incomes_by_category=top_incomes,
            budgets=budgets,
            recent_transactions=recent,
        )