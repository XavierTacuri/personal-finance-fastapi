from datetime import date
from app.schemas.budgets import BudgetStatusOut, BudgetUpsertIn
from app.repositories.budgets_repo import BudgetsRepository


class BudgetsService:
    def __init__(self, repo: BudgetsRepository):
        self.repo = repo

    def upsert(self, user_id: int, payload: BudgetUpsertIn):
        # recomendado: normalizar month al primer día del mes
        normalized_month = payload.month.replace(day=1)
        return self.repo.upsert(
            user_id=user_id,
            category_id=payload.category_id,
            month=normalized_month,
            limit_amount=payload.limit_amount,
        )

    def status(self, user_id: int, month: date):
        normalized_month = month.replace(day=1)

        budgets, spent_map = self.repo.list_for_month(user_id=user_id, month=normalized_month)

        out = []
        for category_id, category_name, month_val, limit_amount in budgets:
            limit_f = float(limit_amount)
            spent = float(spent_map.get(category_id, 0.0))
            remaining = round(limit_f - spent, 2)
            percent_used = round((spent / limit_f * 100.0), 2) if limit_f > 0 else 0.0

            out.append(
                BudgetStatusOut(
                    category_id=category_id,
                    category_name=category_name,
                    month=month_val,
                    limit_amount=limit_f,
                    spent=spent,
                    remaining=remaining,
                    percent_used=percent_used,
                )
            )

        return out