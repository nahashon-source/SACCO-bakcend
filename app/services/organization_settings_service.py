from app.models.settings_model import OrganizationSettings
from app.repositories.mock.settings_repository import MockSettingsRepository


class OrganizationSettingsService:
    def __init__(self, settings_repository: MockSettingsRepository):
        self._settings_repository = settings_repository

    async def get_settings(self) -> OrganizationSettings:
        return await self._settings_repository.get()

    async def update_settings(self, updates: dict) -> OrganizationSettings:
        return await self._settings_repository.update(updates)
