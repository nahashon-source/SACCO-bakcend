from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ContributionType(str, Enum):
    MONTHLY = "monthly"
    SPECIAL = "special"
    WELFARE = "welfare"


class Contribution(BaseModel):
    id: int
    member_id: int
    type: ContributionType
    amount: float
    contributed_at: datetime
    created_at: datetime
