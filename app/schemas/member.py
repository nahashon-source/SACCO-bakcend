from datetime import datetime

from pydantic import EmailStr, Field

from app.models.member import MemberStatus
from app.schemas.base import CamelModel


class MemberOut(CamelModel):
    id: int
    member_number: str
    full_name: str
    email: EmailStr
    phone_number: str
    status: MemberStatus
    joined_at: datetime


class CreateMemberRequest(CamelModel):
    full_name: str = Field(min_length=2)
    email: EmailStr
    phone_number: str = Field(min_length=10)


class UpdateMemberRequest(CamelModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    status: MemberStatus | None = None


class MemberListParams(CamelModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    search: str | None = None
    status: MemberStatus | None = None
