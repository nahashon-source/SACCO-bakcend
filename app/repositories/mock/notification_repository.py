from datetime import datetime, timezone

from app.models.notification import Notification
from app.repositories.base import BaseRepository


def _d(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc)


_notifications: list[Notification] = [
    Notification(id=1, member_id=2, title="Loan application received", message="Your loan application LN-2002 has been received and is under review.", is_read=False, created_at=_d(2026, 6, 20)),
    Notification(id=2, member_id=1, title="Contribution recorded", message="Your monthly contribution of KES 2,000 has been recorded.", is_read=True, created_at=_d(2026, 6, 1)),
    Notification(id=3, member_id=8, title="Loan approved", message="Your loan application LN-2006 has been approved and is pending disbursement.", is_read=False, created_at=_d(2026, 7, 2)),
    Notification(id=4, member_id=6, title="Repayment received", message="Your loan repayment of KES 30,000 has been recorded.", is_read=True, created_at=_d(2026, 5, 1)),
    Notification(id=5, member_id=9, title="Loan application declined", message="Your loan application LN-2007 was not approved. Contact the branch for details.", is_read=False, created_at=_d(2026, 5, 14)),
]


class MockNotificationRepository(BaseRepository[Notification]):
    async def get_by_id(self, entity_id: int) -> Notification | None:
        return next((n for n in _notifications if n.id == entity_id), None)

    async def list_all(self) -> list[Notification]:
        return _notifications

    async def filter(self, is_read: bool | None) -> list[Notification]:
        if is_read is None:
            return _notifications
        return [n for n in _notifications if n.is_read == is_read]

    async def create(self, entity: Notification) -> Notification:
        _notifications.append(entity)
        return entity

    async def update(self, entity_id: int, updates: dict) -> Notification | None:
        notification = await self.get_by_id(entity_id)
        if notification is None:
            return None
        updated = notification.model_copy(update=updates)
        _notifications[_notifications.index(notification)] = updated
        return updated

    async def mark_all_as_read(self) -> None:
        global _notifications
        _notifications = [n.model_copy(update={"is_read": True}) for n in _notifications]

    async def delete(self, entity_id: int) -> bool:
        notification = await self.get_by_id(entity_id)
        if notification is None:
            return False
        _notifications.remove(notification)
        return True


_SEED_NOTIFICATIONS = list(_notifications)


def reset_notification_data() -> None:
    global _notifications
    _notifications = list(_SEED_NOTIFICATIONS)
