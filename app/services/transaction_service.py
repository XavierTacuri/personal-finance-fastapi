
from datetime import date
from typing import List,Optional

from app.schemas.transaction import TransactionCreate,TransactionType,TransactionOut
from app.models.db_models import Transaction

class TransactionService:

    def __init__(self, repo):
        self.repo = repo

    def create_transaction(self, payload:TransactionCreate, user_id: int) -> Transaction:
        return self.repo.create(user_id=user_id,payload=payload)

    def list_transactions(self, user_id: int,
                          tx_type: Optional[TransactionType] = None,
                          category_id: Optional[int] = None,
                          date_from: Optional[date]=None,
                          date_to:Optional[date]=None,) -> List[TransactionOut]:
        return self.repo.get_all(user_id=user_id,
                                 tx_type=tx_type,
                                 category_id=category_id,
                                 date_from=date_from,
                                 date_to=date_to,)