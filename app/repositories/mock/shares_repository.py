from datetime import datetime, timezone

from app.models.shares import ShareAccount
from app.repositories.base import BaseRepository


def _d(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc)


_share_accounts: list[ShareAccount] = [
    ShareAccount(id=1, member_id=1, total_shares=500, share_value=100, purchased_at=_d(2024, 3, 1), created_at=_d(2024, 3, 1), updated_at=_d(2024, 3, 1)),
    ShareAccount(id=2, member_id=2, total_shares=1200, share_value=100, purchased_at=_d(2024, 6, 10), created_at=_d(2024, 6, 10), updated_at=_d(2024, 6, 10)),
    ShareAccount(id=3, member_id=4, total_shares=300, share_value=100, purchased_at=_d(2025, 1, 20), created_at=_d(2025, 1, 20), updated_at=_d(2025, 1, 20)),
    ShareAccount(id=4, member_id=6, total_shares=800, share_value=100, purchased_at=_d(2024, 11, 5), created_at=_d(2024, 11, 5), updated_at=_d(2024, 11, 5)),
    ShareAccount(id=5, member_id=8, total_shares=450, share_value=100, purchased_at=_d(2025, 5, 12), created_at=_d(2025, 5, 12), updated_at=_d(2025, 5, 12)),
    ShareAccount(id=6, member_id=10, total_shares=150, share_value=100, purchased_at=_d(2025, 10, 2), created_at=_d(2025, 10, 2), updated_at=_d(2025, 10, 2)),
]

_next_id = 7


class MockSharesRepository(BaseRepository[ShareAccount]):
    async def get_by_id(self, entity_id: int) -> ShareAccount | None:
        return next((s for s in _share_accounts if s.id == entity_id), None)

    async def list_all(self) -> list[ShareAccount]:
        return _share_accounts

    async def filter(self, member_id: int | None) -> list[ShareAccount]:
        if member_id is None:
            return _share_accounts
        return [s for s in _share_accounts if s.member_id == member_id]

    async def get_by_member_id(self, member_id: int) -> ShareAccount | None:
        return next((s for s in _share_accounts if s.member_id == member_id), None)

    async def create(self, entity: ShareAccount) -> ShareAccount:
        global _next_id
        entity = entity.model_copy(update={"id": _next_id})
        _next_id += 1
        _share_accounts.append(entity)
        return entity

    async def update(self, entity_id: int, updates: dict) -> ShareAccount | None:
        account = await self.get_by_id(entity_id)
        if account is None:
            return None
        updated = account.model_copy(update={**updates, "updated_at": datetime.now(timezone.utc)})
        _share_accounts[_share_accounts.index(account)] = updated
        return updated

    async def delete(self, entity_id: int) -> bool:
        account = await self.get_by_id(entity_id)
        if account is None:
            return False
        _share_accounts.remove(account)
        return True


_SEED_SHARES = list(_share_accounts)


def reset_shares_data() -> None:
    global _share_accounts, _next_id
    _share_accounts = list(_SEED_SHARES)
    _next_id = 7
