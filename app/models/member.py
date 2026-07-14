from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class MemberStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class KYCStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class NextOfKin(BaseModel):
    full_name: str
    relationship: str
    phone_number: str


class EmploymentInfo(BaseModel):
    employer_name: str
    job_title: str
    monthly_income: float


class MemberDocument(BaseModel):
    id: int
    document_type: str
    file_name: str
    uploaded_at: datetime


class Member(BaseModel):
    id: int
    member_number: str
    full_name: str
    email: EmailStr
    phone_number: str
    status: MemberStatus
    branch_id: int | None = None
    kyc_status: KYCStatus = KYCStatus.PENDING
    next_of_kin: NextOfKin | None = None
    employment: EmploymentInfo | None = None
    documents: list[MemberDocument] = []
    joined_at: datetime
    created_at: datetime
    updated_at: datetime
