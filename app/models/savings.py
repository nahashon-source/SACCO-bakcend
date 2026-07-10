from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class SavingsAccountStatus(str, Enum):
    ACTIVE = "active"
    DORMANT = "dormant"
    CLOSED = "closed"


class SavingsAccountType(str, Enum):
    REGULAR = "regular"
    FIXED_DEPOSIT = "fixed_deposit"
    JUNIOR = "junior"


class SavingsAccount(BaseModel):
    id: int
    member_id: int
    account_number: str
    account_type: SavingsAccountType
    balance: float
    status: SavingsAccountStatus
    opened_at: datetime
    created_at: datetime
    updated_at: datetime
