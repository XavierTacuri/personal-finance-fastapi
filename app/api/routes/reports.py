from typing import List

from fastapi import APIRouter,Depends,Query
from datetime import date
from sqlmodel import Session

from app.api.deps import get_session,get_current_user
from app.models.db_models import TransactionType
from app.repositories.reports_repo import ReportsRepository
from app.services.report_service import ReportService
from app.schemas.report import MonthlySummaryOut,CategoryTotalOut,DailyTotalOut

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/monthly-summary",response_model=MonthlySummaryOut)
def monthly_report(year:int =Query(...,ge=2000,le=2100),
                   month:int=Query(...,ge=1,le=12),
                   db:Session=Depends(get_session),
                   user=Depends(get_current_user),):
    service = ReportService(ReportsRepository(db))
    return service.monthly_summary(user_id=user.id,year=year,month=month)

@router.get("/by-category",response_model=list[CategoryTotalOut])
def by_category(year:int =Query(...,ge=2000,le=2100),
                month:int=Query(...,ge=1,le=12),
                type:TransactionType=Query(...),
                db:Session=Depends(get_session),
                user=Depends(get_current_user),):
    service = ReportService(ReportsRepository(db))
    return service.by_category(user_id=user.id,year=year,month=month,tx_type=type)

@router.get("/daily-summary",response_model=list[DailyTotalOut])
def by_daily(from_date:date = Query(...,alias="from"),
             to_date:date = Query(...,alias="to"),
             type:TransactionType=Query(...),
             db:Session=Depends(get_session),
             user=Depends(get_current_user),):
    service = ReportService(ReportsRepository(db))
    return service.daily(user_id=user.id,date_from=from_date,date_to=to_date,tx_type=type)
