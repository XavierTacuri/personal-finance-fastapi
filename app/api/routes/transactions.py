# app/api/routes/transactions.py

from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.transaction import TransactionCreate
from app.repositories.transactions_repo import TransactionRepository
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_service(db: Session = Depends(get_session)):
    repo = TransactionRepository(db)
    return TransactionService(repo)


@router.post("/")
def create_transaction(payload: TransactionCreate, service: TransactionService = Depends(get_service)):
    return service.create_transaction(payload)


@router.get("/{user_id}")
def list_transactions(user_id: int, service: TransactionService = Depends(get_service)):
    return service.list_transactions(user_id)
