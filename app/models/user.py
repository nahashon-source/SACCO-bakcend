"""
Domain entity for a system user (staff/admin who logs into the backend —
distinct from a SACCO "Member", which is a business entity with its own
model in app/models/member.py once that domain is built).

This shape is storage-agnostic: both the mock repository and the future
SQLAlchemy repository must produce/consume objects matching this exact
schema, which is what makes them swappable behind the same interface.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    MEMBER = "member"


class User(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    hashed_password: str
    role: UserRole
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
