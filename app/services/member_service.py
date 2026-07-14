from datetime import datetime, timezone

from app.models.member import Member, MemberStatus
from app.repositories.mock.member_repository import MockMemberRepository


class MemberNotFoundError(Exception):
    pass


class MemberService:
    def __init__(self, member_repository: MockMemberRepository):
        self._member_repository = member_repository

    async def list_members(
        self,
        page: int,
        page_size: int,
        search: str | None,
        status: MemberStatus | None,
        branch_id: int | None = None,
    ) -> tuple[list[Member], int]:
        all_matching = await self._member_repository.search(search, status, branch_id)
        total_items = len(all_matching)

        start = (page - 1) * page_size
        end = start + page_size
        page_items = all_matching[start:end]

        return page_items, total_items

    async def get_member(self, member_id: int) -> Member:
        member = await self._member_repository.get_by_id(member_id)
        if member is None:
            raise MemberNotFoundError(f"Member with id {member_id} not found")
        return member

    async def create_member(
        self, full_name: str, email: str, phone_number: str, branch_id: int | None = None
    ) -> Member:
        existing_count = len(await self._member_repository.list_all())
        member_number = f"MEM-{existing_count + 1:04d}"

        now = datetime.now(timezone.utc)
        new_member = Member(
            id=0,
            member_number=member_number,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            status=MemberStatus.ACTIVE,
            branch_id=branch_id,
            joined_at=now,
            created_at=now,
            updated_at=now,
        )

        return await self._member_repository.create(new_member)

    async def update_member(self, member_id: int, updates: dict) -> Member:
        clean_updates = {k: v for k, v in updates.items() if v is not None}
        updated = await self._member_repository.update(member_id, clean_updates)
        if updated is None:
            raise MemberNotFoundError(f"Member with id {member_id} not found")
        return updated

    async def delete_member(self, member_id: int) -> None:
        deleted = await self._member_repository.delete(member_id)
        if not deleted:
            raise MemberNotFoundError(f"Member with id {member_id} not found")
