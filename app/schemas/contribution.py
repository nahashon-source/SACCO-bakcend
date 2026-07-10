from datetime import datetime

from pydantic import Field

from app.models.contribution import ContributionType
from app.schemas.base import CamelModel


class ContributionOut(CamelModel):
    id: int
    member_id: int
    type: ContributionType
    amount: float
    contributed_at: datetime


class RecordContributionRequest(CamelModel):
    member_id: int
    type: ContributionType
    amount: float = Field(gt=0)
