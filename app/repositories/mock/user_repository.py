"""
In-memory User repository. Active when settings.USE_MOCK_DATA is True.
Data resets on every server restart — that's expected and fine for
frontend-only development; nothing here is meant to persist.
"""

from datetime import datetime, timezone

from app.core.security import hash_password
from app.models.user import User, UserRole
from app.repositories.base import BaseRepository

_now = datetime.now(timezone.utc)

_users: list[User] = [
    User(
        id=1,
        full_name="Demo Staff",
        email="staff@fitsacco.example.com",
        hashed_password=hash_password("Password123!"),
        role=UserRole.STAFF,
        is_active=True,
        created_at=_now,
        updated_at=_now,
    )
]


class MockUserRepository(BaseRepository[User]):
    async def get_by_id(self, entity_id: int) -> User | None:
        return next((u for u in _users if u.id == entity_id), None)

    async def get_by_email(self, email: str) -> User | None:
        return next((u for u in _users if u.email == email), None)

    async def list_all(self) -> list[User]:
        return _users

    async def create(self, entity: User) -> User:
        _users.append(entity)
        return entity

    async def update(self, entity_id: int, updates: dict) -> User | None:
        user = await self.get_by_id(entity_id)
        if user is None:
            return None
        updated = user.model_copy(update=updates)
        _users[_users.index(user)] = updated
        return updated

    async def delete(self, entity_id: int) -> bool:
        user = await self.get_by_id(entity_id)
        if user is None:
            return False
        _users.remove(user)
        return True


def reset_user_data() -> None:
    """Restore seed data. Called between tests for isolation — see tests/conftest.py."""
    global _users
    _users = [
        User(
            id=1,
            full_name="Demo Staff",
            email="staff@fitsacco.example.com",
            hashed_password=hash_password("Password123!"),
            role=UserRole.STAFF,
            is_active=True,
            created_at=_now,
            updated_at=_now,
        )
    ]
