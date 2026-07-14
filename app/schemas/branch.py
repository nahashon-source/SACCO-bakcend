from app.models.branch import BranchStatus
from app.schemas.base import CamelModel


class BranchOut(CamelModel):
    id: int
    name: str
    code: str
    address: str
    manager_member_id: int | None
    status: BranchStatus


class CreateBranchRequest(CamelModel):
    name: str
    code: str
    address: str
    manager_member_id: int | None = None


class UpdateBranchRequest(CamelModel):
    name: str | None = None
    address: str | None = None
    manager_member_id: int | None = None
    status: BranchStatus | None = None
