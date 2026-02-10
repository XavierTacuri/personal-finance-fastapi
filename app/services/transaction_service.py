from datetime import date
from typing import List, Optional

from app.schemas.transaction import TransactionType,TransactionOut,TransactionCreate,Category
from app.repositories.transactions_repo import TransactionRepository

class TransactionService:

    def __init__(self,repo: TransactionRepository)->None:
        self.repo = repo

    def create_transaction(self, payload : TransactionCreate)->TransactionOut:
        return self.repo.create(payload)

    def list_transactions(self,
                          tx_type: Optional[TransactionType]=None,
                          category: Optional[Category]=None,
                          date_from: Optional[date]=None,
                          date_to: Optional[date]=None)->List[TransactionOut]:
        return self.repo.list(tx_type=tx_type,
                              category=category,
                              date_from=date_from,
                              date_to=date_to)