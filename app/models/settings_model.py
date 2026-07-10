"""
Domain entity for organization settings. A singleton — there is exactly
one OrganizationSettings record for the whole SACCO, unlike every other
domain modeled so far which has many records. The mock repository
reflects that (get/update only, no list, no id parameter needed).
"""

from datetime import datetime

from pydantic import BaseModel


class OrganizationSettings(BaseModel):
    organization_name: str
    registration_number: str
    contact_email: str
    contact_phone: str
    updated_at: datetime
