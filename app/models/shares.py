from datetime import datetime

from pydantic import BaseModel


class ShareAccount(BaseModel):
    id: int
    member_id: int
    total_shares: int
    share_value: float
    purchased_at: datetime
    created_at: datetime
    updated_at: datetime

    @property
    def total_value(self) -> float:
        return self.total_shares * self.share_value
