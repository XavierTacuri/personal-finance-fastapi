from fastapi import APIRouter,Depends
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.report import monthlyReport
from app.repositories.reports_repo import ReportsRepository
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])

def get_service(db: Session = Depends(get_session)):
    return ReportService(ReportsRepository(db))

@router.get("/",response_model=monthlyReport)
def monthly_report(user_id:int, year:int, month:int,service:ReportService=Depends(get_service)):
    return service.monthly_report(user_id,year,month)
