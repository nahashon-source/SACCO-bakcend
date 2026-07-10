"""
Domain entity for a SACCO member. Storage-agnostic — mock and future
real repositories both produce/consume this exact shape.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class MemberStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class Member(BaseModel):
    id: int
    member_number: str
    full_name: str
    email: EmailStr
    phone_number: str
    status: MemberStatus
    joined_at: datetime
    created_at: datetime
    updated_at: datetime
