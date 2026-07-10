from datetime import datetime

from pydantic import Field

from app.models.loan import LoanStatus
from app.schemas.base import CamelModel


class LoanOut(CamelModel):
    id: int
    loan_number: str
    member_id: int
    principal: float
    interest_rate: float
    term_months: int
    outstanding_balance: float
    status: LoanStatus
    applied_at: datetime
    disbursed_at: datetime | None


class LoanApplicationRequest(CamelModel):
    member_id: int
    principal: float = Field(gt=0)
    term_months: int = Field(gt=0)
    purpose: str = Field(min_length=5)


class LoanRejectRequest(CamelModel):
    reason: str = Field(min_length=5)


class LoanRepaymentRequest(CamelModel):
    amount: float = Field(gt=0)
    reference: str | None = None
