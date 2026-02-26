from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.deps import get_session, get_current_user
from app.schemas.dashboard import DashboardOut
from app.repositories.dashboard_repo import DashboardRepository
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardOut)
def dashboard(
    month: date = Query(...),          # "2026-02-01"
    top_n: int = Query(5, ge=1, le=20),
    recent_n: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    service = DashboardService(DashboardRepository(db))
    return service.get_dashboard(user_id=user.id, month=month, top_n=top_n, recent_n=recent_n)