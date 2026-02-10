from datetime import date
from typing import Optional, List
from unittest import result

from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionType,Category

class TransactionRepository:

    def __init__(self)->None:
        self._data: List[TransactionOut] = []
        self._id: int = 1

    def create(self, payload: TransactionCreate)->TransactionOut:
        item = TransactionOut(id=self._id, **payload.model_dump())
        self._id += 1
        self._data.append(item)
        return item

    def list(self,
             tx_type: Optional[TransactionType]=None,
             category: Optional[Category]=None,
             date_from: Optional[date]=None,
             date_to: Optional[date]=None,)-> List[TransactionOut]:
        result = self._data

        if tx_type:
            result=[x for x in result if x.type == tx_type]
        if category:
            result=[x for x in result if x.category == category]
        if date_from:
            result=[x for x in result if x.date >= date_from ]
        if date_to:
            result=[x for x in result if x.date <= date_to ]

        return result


