# app/api/routes/transactions.py
from datetime import date
from typing import List,Optional

from fastapi import APIRouter, Depends,HTTPException,Query
from sqlmodel import Session
from app.api.deps import get_current_user
from app.db.session import get_session

from app.repositories.transactions_repo import TransactionRepository
from app.schemas.common import Page
from app.services.transaction_service import TransactionService
from app.schemas.transaction import TransactionCreate,TransactionType,TransactionOut
from app.models.db_models import Transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("", response_model=TransactionOut, status_code=201)
def create_transaction(payload: TransactionCreate,
                       db: Session = Depends(get_session),
                       user=Depends(get_current_user)):
    service = TransactionService(TransactionRepository(db))
    try:
        return service.create_transaction(user_id=user.id,payload=payload)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))


@router.get("",response_model=Page[TransactionOut])
def list_transactions(
    type: TransactionType | None = Query(None),
    category_id: int | None = Query(None),
    from_date: date | None = Query(None, alias="from"),
    to_date: date | None = Query(None, alias="to"),
    sort: str = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_session),
    user=Depends(get_current_user),
    ):
    service = TransactionService(TransactionRepository(db))
    items, total = service.list_page(
        user_id=user.id,
        tx_type=type,
        category_id=category_id,
        date_from=from_date,
        date_to=to_date,
        sort=sort,
        limit=limit,
        offset=offset,
    )
    return {"items": items, "total": total, "limit": limit, "offset": offset}
