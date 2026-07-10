from datetime import datetime

from pydantic import Field

from app.models.savings import SavingsAccountStatus, SavingsAccountType
from app.schemas.base import CamelModel


class SavingsAccountOut(CamelModel):
    id: int
    member_id: int
    account_number: str
    account_type: SavingsAccountType
    balance: float
    status: SavingsAccountStatus
    opened_at: datetime


class CreateSavingsAccountRequest(CamelModel):
    member_id: int
    account_type: SavingsAccountType


class SavingsDepositRequest(CamelModel):
    amount: float = Field(gt=0)
    reference: str | None = None


class SavingsWithdrawalRequest(CamelModel):
    amount: float = Field(gt=0)
    reason: str = Field(min_length=3)
