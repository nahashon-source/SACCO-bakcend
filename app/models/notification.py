from datetime import datetime

from pydantic import BaseModel


class Notification(BaseModel):
    id: int
    member_id: int | None = None  # None = system-wide / staff notification, not tied to a specific member
    title: str
    message: str
    is_read: bool = False
    created_at: datetime
