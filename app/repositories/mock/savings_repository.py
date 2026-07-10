from datetime import datetime, timezone

from app.models.savings import SavingsAccount, SavingsAccountStatus, SavingsAccountType
from app.repositories.base import BaseRepository

_savings_accounts: list[SavingsAccount] = [
    SavingsAccount(
        id=1,
        member_id=1,
        account_number="SAV-1001",
        account_type=SavingsAccountType.REGULAR,
        balance=84500,
        status=SavingsAccountStatus.ACTIVE,
        opened_at=datetime(2024, 2, 15, tzinfo=timezone.utc),
        created_at=datetime(2024, 2, 15, tzinfo=timezone.utc),
        updated_at=datetime(2024, 2, 15, tzinfo=timezone.utc),
    ),
    SavingsAccount(
        id=2,
        member_id=2,
        account_number="SAV-1002",
        account_type=SavingsAccountType.FIXED_DEPOSIT,
        balance=250000,
        status=SavingsAccountStatus.ACTIVE,
        opened_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
        created_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
        updated_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
    ),
    SavingsAccount(
        id=3,
        member_id=3,
        account_number="SAV-1003",
        account_type=SavingsAccountType.REGULAR,
        balance=12300,
        status=SavingsAccountStatus.DORMANT,
        opened_at=datetime(2023, 12, 1, tzinfo=timezone.utc),
        created_at=datetime(2023, 12, 1, tzinfo=timezone.utc),
        updated_at=datetime(2023, 12, 1, tzinfo=timezone.utc),
    ),
]

_next_id = 4


class MockSavingsRepository(BaseRepository[SavingsAccount]):
    async def get_by_id(self, entity_id: int) -> SavingsAccount | None:
        return next((a for a in _savings_accounts if a.id == entity_id), None)

    async def list_all(self) -> list[SavingsAccount]:
        return _savings_accounts

    async def filter(self, member_id: int | None) -> list[SavingsAccount]:
        if member_id is None:
            return _savings_accounts
        return [a for a in _savings_accounts if a.member_id == member_id]

    async def create(self, entity: SavingsAccount) -> SavingsAccount:
        global _next_id
        entity = entity.model_copy(update={"id": _next_id})
        _next_id += 1
        _savings_accounts.append(entity)
        return entity

    async def update(self, entity_id: int, updates: dict) -> SavingsAccount | None:
        account = await self.get_by_id(entity_id)
        if account is None:
            return None
        updated = account.model_copy(
            update={**updates, "updated_at": datetime.now(timezone.utc)}
        )
        _savings_accounts[_savings_accounts.index(account)] = updated
        return updated

    async def delete(self, entity_id: int) -> bool:
        account = await self.get_by_id(entity_id)
        if account is None:
            return False
        _savings_accounts.remove(account)
        return True


_SEED_SAVINGS = list(_savings_accounts)


def reset_savings_data() -> None:
    """Restore seed data. Called between tests for isolation."""
    global _savings_accounts, _next_id
    _savings_accounts = list(_SEED_SAVINGS)
    _next_id = 4
