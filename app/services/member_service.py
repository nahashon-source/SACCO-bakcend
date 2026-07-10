"""
Member business logic. Routes call this service; the service calls the
repository. Includes pagination and member-number generation — rules
that don't belong in the repository (pure data access) or the route
(thin, HTTP-only).
"""

import math
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
    ) -> tuple[list[Member], int]:
        all_matching = await self._member_repository.search(search, status)
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

    async def create_member(self, full_name: str, email: str, phone_number: str) -> Member:
        existing_count = len(await self._member_repository.list_all())
        member_number = f"MEM-{existing_count + 1:04d}"

        now = datetime.now(timezone.utc)
        new_member = Member(
            id=0,  # overwritten by repository on create
            member_number=member_number,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            status=MemberStatus.ACTIVE,
            joined_at=now,
            created_at=now,
            updated_at=now,
        )

        return await self._member_repository.create(new_member)

    async def update_member(self, member_id: int, updates: dict) -> Member:
        # Filter out None values so partial updates (PATCH semantics)
        # don't overwrite existing fields with null.
        clean_updates = {k: v for k, v in updates.items() if v is not None}

        updated = await self._member_repository.update(member_id, clean_updates)
        if updated is None:
            raise MemberNotFoundError(f"Member with id {member_id} not found")
        return updated

    async def delete_member(self, member_id: int) -> None:
        deleted = await self._member_repository.delete(member_id)
        if not deleted:
            raise MemberNotFoundError(f"Member with id {member_id} not found")
