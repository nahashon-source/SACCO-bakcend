from datetime import datetime

from app.models.transaction import TransactionStatus, TransactionType
from app.schemas.base import CamelModel


class TransactionOut(CamelModel):
    id: int
    member_id: int
    type: TransactionType
    amount: float
    status: TransactionStatus
    reference: str
    created_at: datetime
