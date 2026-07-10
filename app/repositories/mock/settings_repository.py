"""
In-memory OrganizationSettings repository. Singleton pattern — get()
and update() only, no create/delete/list, since there's exactly one
record.
"""

from datetime import datetime, timezone

from app.models.settings_model import OrganizationSettings

_settings = OrganizationSettings(
    organization_name="Freight in Time SACCO",
    registration_number="SACCO-KE-4471",
    contact_email="info@fitsacco.example.com",
    contact_phone="+254700123456",
    updated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
)


class MockSettingsRepository:
    async def get(self) -> OrganizationSettings:
        return _settings

    async def update(self, updates: dict) -> OrganizationSettings:
        global _settings
        clean_updates = {k: v for k, v in updates.items() if v is not None}
        _settings = _settings.model_copy(
            update={**clean_updates, "updated_at": datetime.now(timezone.utc)}
        )
        return _settings


_SEED_SETTINGS = _settings.model_copy()


def reset_settings_data() -> None:
    """Restore seed data. Called between tests for isolation."""
    global _settings
    _settings = _SEED_SETTINGS.model_copy()
