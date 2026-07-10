"""
Domain entity for a Loan. Status transitions (pending -> approved ->
disbursed, or pending -> rejected) are enforced in the service layer,
not here — this model only describes shape, not behavior.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class LoanStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DISBURSED = "disbursed"
    REJECTED = "rejected"
    CLOSED = "closed"
    DEFAULTED = "defaulted"


class Loan(BaseModel):
    id: int
    loan_number: str
    member_id: int
    principal: float
    interest_rate: float
    term_months: int
    outstanding_balance: float
    status: LoanStatus
    applied_at: datetime
    disbursed_at: datetime | None = None
    rejection_reason: str | None = None
    created_at: datetime
    updated_at: datetime
