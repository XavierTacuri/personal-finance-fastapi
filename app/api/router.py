from fastapi import APIRouter
from app.api.routes.transactions import router as transaction_router

api_router = APIRouter()
api_router.include_router(transaction_router)