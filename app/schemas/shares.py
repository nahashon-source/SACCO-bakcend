from datetime import datetime

from pydantic import Field

from app.schemas.base import CamelModel


class ShareAccountOut(CamelModel):
    id: int
    member_id: int
    total_shares: int
    share_value: float
    total_value: float
    purchased_at: datetime


class PurchaseSharesRequest(CamelModel):
    member_id: int
    number_of_shares: int = Field(gt=0)
