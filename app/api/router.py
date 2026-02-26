from fastapi import APIRouter
from app.api.routes import transactions, users, reports
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.categories import router as categories_router
from app.api.routes.budgets import router as budgets_router
from app.api.routes.reports import router as reports_router
from app.api.routes.dashboard import router as dashboard_router
#from app.api.routes.reports import router as report_router

api_router = APIRouter()
api_router.include_router(transactions.router)
api_router.include_router(users.router)
api_router.include_router(reports.router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(categories_router)
api_router.include_router(budgets_router)
api_router.include_router(reports_router)
api_router.include_router(dashboard_router)
#api_router.include_router(report_router)