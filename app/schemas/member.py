from datetime import datetime

from pydantic import EmailStr, Field

from app.models.member import KYCStatus, MemberStatus
from app.schemas.base import CamelModel


class NextOfKinSchema(CamelModel):
    full_name: str
    relationship: str
    phone_number: str


class EmploymentInfoSchema(CamelModel):
    employer_name: str
    job_title: str
    monthly_income: float


class MemberDocumentOut(CamelModel):
    id: int
    document_type: str
    file_name: str
    uploaded_at: datetime


class MemberOut(CamelModel):
    id: int
    member_number: str
    full_name: str
    email: EmailStr
    phone_number: str
    status: MemberStatus
    branch_id: int | None
    kyc_status: KYCStatus
    next_of_kin: NextOfKinSchema | None
    employment: EmploymentInfoSchema | None
    documents: list[MemberDocumentOut]
    joined_at: datetime


class CreateMemberRequest(CamelModel):
    full_name: str = Field(min_length=2)
    email: EmailStr
    phone_number: str = Field(min_length=10)
    branch_id: int | None = None


class UpdateMemberRequest(CamelModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    status: MemberStatus | None = None
    branch_id: int | None = None
    kyc_status: KYCStatus | None = None


class UpdateNextOfKinRequest(CamelModel):
    full_name: str = Field(min_length=2)
    relationship: str = Field(min_length=2)
    phone_number: str = Field(min_length=10)


class UpdateEmploymentInfoRequest(CamelModel):
    employer_name: str = Field(min_length=2)
    job_title: str = Field(min_length=2)
    monthly_income: float = Field(ge=0)


class MemberListParams(CamelModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    search: str | None = None
    status: MemberStatus | None = None
    branch_id: int | None = None
