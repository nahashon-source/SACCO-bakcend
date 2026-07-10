"""
In-memory Member repository. Active when settings.USE_MOCK_DATA is True.
Seed data intentionally mirrors the frontend's src/mocks/data.ts fixtures
so the two mock layers (frontend MSW, backend mock repo) show consistent
demo data if someone compares them side by side.
"""

from datetime import datetime, timezone

from app.models.member import Member, MemberStatus
from app.repositories.base import BaseRepository

_members: list[Member] = [
    Member(
        id=1,
        member_number="MEM-0001",
        full_name="Wanjiru Kamau",
        email="wanjiru.kamau@example.com",
        phone_number="+254712345001",
        status=MemberStatus.ACTIVE,
        joined_at=datetime(2024, 2, 14, tzinfo=timezone.utc),
        created_at=datetime(2024, 2, 14, tzinfo=timezone.utc),
        updated_at=datetime(2024, 2, 14, tzinfo=timezone.utc),
    ),
    Member(
        id=2,
        member_number="MEM-0002",
        full_name="Otieno Odhiambo",
        email="otieno.odhiambo@example.com",
        phone_number="+254712345002",
        status=MemberStatus.ACTIVE,
        joined_at=datetime(2024, 5, 3, tzinfo=timezone.utc),
        created_at=datetime(2024, 5, 3, tzinfo=timezone.utc),
        updated_at=datetime(2024, 5, 3, tzinfo=timezone.utc),
    ),
    Member(
        id=3,
        member_number="MEM-0003",
        full_name="Achieng Njoroge",
        email="achieng.njoroge@example.com",
        phone_number="+254712345003",
        status=MemberStatus.INACTIVE,
        joined_at=datetime(2023, 11, 20, tzinfo=timezone.utc),
        created_at=datetime(2023, 11, 20, tzinfo=timezone.utc),
        updated_at=datetime(2023, 11, 20, tzinfo=timezone.utc),
    ),
    Member(
        id=4,
        member_number="MEM-0004",
        full_name="Mutiso Kiplagat",
        email="mutiso.kiplagat@example.com",
        phone_number="+254712345004",
        status=MemberStatus.ACTIVE,
        joined_at=datetime(2025, 1, 9, tzinfo=timezone.utc),
        created_at=datetime(2025, 1, 9, tzinfo=timezone.utc),
        updated_at=datetime(2025, 1, 9, tzinfo=timezone.utc),
    ),
]

_next_id = 5


class MockMemberRepository(BaseRepository[Member]):
    async def get_by_id(self, entity_id: int) -> Member | None:
        return next((m for m in _members if m.id == entity_id), None)

    async def list_all(self) -> list[Member]:
        return _members

    async def search(self, search: str | None, status: MemberStatus | None) -> list[Member]:
        results = _members

        if status is not None:
            results = [m for m in results if m.status == status]

        if search:
            search_lower = search.lower()
            results = [
                m
                for m in results
                if search_lower in m.full_name.lower()
                or search_lower in m.member_number.lower()
                or search_lower in m.email.lower()
            ]

        return results

    async def create(self, entity: Member) -> Member:
        global _next_id
        entity = entity.model_copy(update={"id": _next_id})
        _next_id += 1
        _members.append(entity)
        return entity

    async def update(self, entity_id: int, updates: dict) -> Member | None:
        member = await self.get_by_id(entity_id)
        if member is None:
            return None
        updated = member.model_copy(
            update={**updates, "updated_at": datetime.now(timezone.utc)}
        )
        _members[_members.index(member)] = updated
        return updated

    async def delete(self, entity_id: int) -> bool:
        member = await self.get_by_id(entity_id)
        if member is None:
            return False
        _members.remove(member)
        return True


_SEED_MEMBERS = list(_members)


def reset_member_data() -> None:
    """Restore seed data. Called between tests for isolation — see tests/conftest.py."""
    global _members, _next_id
    _members = list(_SEED_MEMBERS)
    _next_id = 5
