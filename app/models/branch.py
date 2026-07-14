from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class BranchStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Branch(BaseModel):
    id: int
    name: str
    code: str
    address: str
    manager_member_id: int | None = None  # references a Member acting as branch manager, optional
    status: BranchStatus
    created_at: datetime
    updated_at: datetime
