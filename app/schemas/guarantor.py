from datetime import datetime

from pydantic import Field

from app.models.guarantor import GuarantorStatus
from app.schemas.base import CamelModel


class GuarantorOut(CamelModel):
    id: int
    loan_id: int
    member_id: int
    guaranteed_amount: float
    status: GuarantorStatus
    responded_at: datetime | None


class AddGuarantorRequest(CamelModel):
    loan_id: int
    member_id: int
    guaranteed_amount: float = Field(gt=0)


class GuarantorRespondRequest(CamelModel):
    accept: bool
