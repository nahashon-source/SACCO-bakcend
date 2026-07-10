from fastapi import APIRouter, Depends

from app.repositories.factory import get_settings_repository
from app.schemas.common import ApiResponse
from app.schemas.settings_schema import OrganizationSettingsOut, UpdateOrganizationSettingsRequest
from app.services.organization_settings_service import OrganizationSettingsService

router = APIRouter(prefix="/settings", tags=["Settings"])


def get_organization_settings_service() -> OrganizationSettingsService:
    return OrganizationSettingsService(settings_repository=get_settings_repository())


@router.get("", response_model=ApiResponse[OrganizationSettingsOut])
async def get_settings(
    settings_service: OrganizationSettingsService = Depends(get_organization_settings_service),
):
    org_settings = await settings_service.get_settings()

    return ApiResponse(
        success=True,
        message="Settings retrieved",
        data=OrganizationSettingsOut.model_validate(org_settings),
    )


@router.patch("", response_model=ApiResponse[OrganizationSettingsOut])
async def update_settings(
    payload: UpdateOrganizationSettingsRequest,
    settings_service: OrganizationSettingsService = Depends(get_organization_settings_service),
):
    updated = await settings_service.update_settings(payload.model_dump())

    return ApiResponse(
        success=True, message="Settings updated", data=OrganizationSettingsOut.model_validate(updated)
    )
