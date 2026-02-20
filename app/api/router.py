from fastapi import APIRouter
from app.api.routes import transactions, users, reports
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router

#from app.api.routes.reports import router as report_router

api_router = APIRouter()
api_router.include_router(transactions.router)
api_router.include_router(users.router)
api_router.include_router(reports.router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
#api_router.include_router(report_router)