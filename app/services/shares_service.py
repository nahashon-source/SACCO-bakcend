"""
Shares business logic. A member has at most one running share account —
purchases add to total_shares on the existing account, or create the
account on first purchase. This differs from Loans/Savings, where
multiple separate accounts per member are normal.
"""

from datetime import datetime, timezone

from app.models.shares import ShareAccount
from app.repositories.mock.member_repository import MockMemberRepository
from app.repositories.mock.shares_repository import MockSharesRepository

DEFAULT_SHARE_VALUE = 100.0


class MemberNotFoundForSharesError(Exception):
    pass


class SharesService:
    def __init__(self, shares_repository: MockSharesRepository, member_repository: MockMemberRepository):
        self._shares_repository = shares_repository
        self._member_repository = member_repository

    async def list_accounts(self, member_id: int | None) -> list[ShareAccount]:
        return await self._shares_repository.filter(member_id)

    async def purchase(self, member_id: int, number_of_shares: int) -> ShareAccount:
        member = await self._member_repository.get_by_id(member_id)
        if member is None:
            raise MemberNotFoundForSharesError(f"Member with id {member_id} does not exist")

        existing = await self._shares_repository.get_by_member_id(member_id)

        if existing is not None:
            new_total = existing.total_shares + number_of_shares
            return await self._shares_repository.update(existing.id, {"total_shares": new_total})

        now = datetime.now(timezone.utc)
        new_account = ShareAccount(
            id=0,  # overwritten by repository
            member_id=member_id,
            total_shares=number_of_shares,
            share_value=DEFAULT_SHARE_VALUE,
            purchased_at=now,
            created_at=now,
            updated_at=now,
        )
        return await self._shares_repository.create(new_account)
