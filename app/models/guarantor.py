from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class GuarantorStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    RELEASED = "released"


class Guarantor(BaseModel):
    id: int
    loan_id: int
    member_id: int
    guaranteed_amount: float
    status: GuarantorStatus
    responded_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
