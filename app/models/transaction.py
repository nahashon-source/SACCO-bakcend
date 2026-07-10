from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    LOAN_DISBURSEMENT = "loan_disbursement"
    LOAN_REPAYMENT = "loan_repayment"
    SHARE_PURCHASE = "share_purchase"
    CONTRIBUTION = "contribution"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"


class Transaction(BaseModel):
    id: int
    member_id: int
    type: TransactionType
    amount: float
    status: TransactionStatus
    reference: str
    created_at: datetime
