from app.models.notification import Notification
from app.repositories.mock.notification_repository import MockNotificationRepository


class NotificationNotFoundError(Exception):
    pass


class NotificationService:
    def __init__(self, notification_repository: MockNotificationRepository):
        self._notification_repository = notification_repository

    async def list_notifications(self, is_read: bool | None) -> list[Notification]:
        return await self._notification_repository.filter(is_read)

    async def mark_as_read(self, notification_id: int) -> Notification:
        updated = await self._notification_repository.update(notification_id, {"is_read": True})
        if updated is None:
            raise NotificationNotFoundError(f"Notification {notification_id} not found")
        return updated

    async def mark_all_as_read(self) -> None:
        await self._notification_repository.mark_all_as_read()
