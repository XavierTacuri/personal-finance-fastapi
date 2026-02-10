from datetime import date
from typing import List,Optional

from fastapi import APIRouter, Query

from app.schemas.transaction import TransactionCreate, TransactionOut,TransactionType,Category
from app.repositories.transactions_repo import TransactionRepository
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])

_repo = TransactionRepository()
_service = TransactionService(_repo)

@router.post("", response_model=TransactionOut, status_code=201)
def create_transaction(payload: TransactionCreate):
    return _service.create_transaction(payload)

@router.get("", response_model=List[TransactionOut])
def list_transactions(type: Optional[TransactionType] = Query(None),
                      category: Optional[Category] = Query(None),
                      from_date: Optional[date] = Query(None, alias="from"),
                      to_date: Optional[date] = Query(None, alias="to")):
    return _service.list_transactions(tx_type =type,
                                      category = category)