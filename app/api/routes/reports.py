from fastapi import APIRouter,Query

from app.schemas.report import MonthlyReport
from app.core.container import report_service


router = APIRouter(prefix="/reports", tags=["reports"])



@router.get("/monthly", response_model=MonthlyReport)
def get_monthly_report(month:str=Query(...,pattern=r"^\d{4}-\d{2}$")):
    return report_service.monthly_report(month)

