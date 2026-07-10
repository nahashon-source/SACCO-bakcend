from app.schemas.base import CamelModel


class OrganizationSettingsOut(CamelModel):
    organization_name: str
    registration_number: str
    contact_email: str
    contact_phone: str


class UpdateOrganizationSettingsRequest(CamelModel):
    organization_name: str | None = None
    registration_number: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
