from datetime import datetime, timezone

from app.models.savings import SavingsAccount, SavingsAccountStatus, SavingsAccountType
from app.repositories.base import BaseRepository


def _d(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc)


_savings_accounts: list[SavingsAccount] = [
    SavingsAccount(id=1, member_id=1, account_number="SAV-1001", account_type=SavingsAccountType.REGULAR, balance=84500, status=SavingsAccountStatus.ACTIVE, opened_at=_d(2024, 2, 15), created_at=_d(2024, 2, 15), updated_at=_d(2024, 2, 15)),
    SavingsAccount(id=2, member_id=2, account_number="SAV-1002", account_type=SavingsAccountType.FIXED_DEPOSIT, balance=250000, status=SavingsAccountStatus.ACTIVE, opened_at=_d(2024, 6, 1), created_at=_d(2024, 6, 1), updated_at=_d(2024, 6, 1)),
    SavingsAccount(id=3, member_id=3, account_number="SAV-1003", account_type=SavingsAccountType.REGULAR, balance=12300, status=SavingsAccountStatus.DORMANT, opened_at=_d(2023, 12, 1), created_at=_d(2023, 12, 1), updated_at=_d(2023, 12, 1)),
    SavingsAccount(id=4, member_id=4, account_number="SAV-1004", account_type=SavingsAccountType.REGULAR, balance=45200, status=SavingsAccountStatus.ACTIVE, opened_at=_d(2025, 1, 10), created_at=_d(2025, 1, 10), updated_at=_d(2025, 1, 10)),
    SavingsAccount(id=5, member_id=5, account_number="SAV-1005", account_type=SavingsAccountType.JUNIOR, balance=8900, status=SavingsAccountStatus.ACTIVE, opened_at=_d(2024, 8, 25), created_at=_d(2024, 8, 25), updated_at=_d(2024, 8, 25)),
    SavingsAccount(id=6, member_id=6, account_number="SAV-1006", account_type=SavingsAccountType.REGULAR, balance=132000, status=SavingsAccountStatus.ACTIVE, opened_at=_d(2024, 10, 6), created_at=_d(2024, 10, 6), updated_at=_d(2024, 10, 6)),
    SavingsAccount(id=7, member_id=8, account_number="SAV-1007", account_type=SavingsAccountType.FIXED_DEPOSIT, balance=310000, status=SavingsAccountStatus.ACTIVE, opened_at=_d(2025, 4, 2), created_at=_d(2025, 4, 2), updated_at=_d(2025, 4, 2)),
    SavingsAccount(id=8, member_id=9, account_number="SAV-1008", account_type=SavingsAccountType.REGULAR, balance=27600, status=SavingsAccountStatus.ACTIVE, opened_at=_d(2025, 7, 15), created_at=_d(2025, 7, 15), updated_at=_d(2025, 7, 15)),
    SavingsAccount(id=9, member_id=11, account_number="SAV-1009", account_type=SavingsAccountType.REGULAR, balance=3100, status=SavingsAccountStatus.DORMANT, opened_at=_d(2024, 4, 20), created_at=_d(2024, 4, 20), updated_at=_d(2024, 4, 20)),
]

_next_id = 10


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
        updated = account.model_copy(update={**updates, "updated_at": datetime.now(timezone.utc)})
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
    global _savings_accounts, _next_id
    _savings_accounts = list(_SEED_SAVINGS)
    _next_id = 10
