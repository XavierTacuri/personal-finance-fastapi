from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.deps import get_session, get_current_user
from app.schemas.budgets import BudgetUpsertIn, BudgetStatusOut
from app.repositories.budgets_repo import BudgetsRepository
from app.services.budgets_service import BudgetsService


router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("", status_code=201)
def upsert_budget(
    payload: BudgetUpsertIn,
    db: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    service = BudgetsService(BudgetsRepository(db))
    return service.upsert(user_id=user.id, payload=payload)


@router.get("", response_model=list[BudgetStatusOut])
def list_budget_status(
    month: date = Query(...),  # "2026-02-01"
    db: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    service = BudgetsService(BudgetsRepository(db))
    return service.status(user_id=user.id, month=month)