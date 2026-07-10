"""
In-memory Member repository. Active when settings.USE_MOCK_DATA is True.
Data resets on every server restart.
"""

from datetime import datetime, timezone

from app.models.member import Member, MemberStatus
from app.repositories.base import BaseRepository


def _d(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc)


_members: list[Member] = [
    Member(id=1, member_number="MEM-0001", full_name="Wanjiru Kamau", email="wanjiru.kamau@example.com", phone_number="+254712345001", status=MemberStatus.ACTIVE, joined_at=_d(2024, 2, 14), created_at=_d(2024, 2, 14), updated_at=_d(2024, 2, 14)),
    Member(id=2, member_number="MEM-0002", full_name="Otieno Odhiambo", email="otieno.odhiambo@example.com", phone_number="+254712345002", status=MemberStatus.ACTIVE, joined_at=_d(2024, 5, 3), created_at=_d(2024, 5, 3), updated_at=_d(2024, 5, 3)),
    Member(id=3, member_number="MEM-0003", full_name="Achieng Njoroge", email="achieng.njoroge@example.com", phone_number="+254712345003", status=MemberStatus.INACTIVE, joined_at=_d(2023, 11, 20), created_at=_d(2023, 11, 20), updated_at=_d(2023, 11, 20)),
    Member(id=4, member_number="MEM-0004", full_name="Mutiso Kiplagat", email="mutiso.kiplagat@example.com", phone_number="+254712345004", status=MemberStatus.ACTIVE, joined_at=_d(2025, 1, 9), created_at=_d(2025, 1, 9), updated_at=_d(2025, 1, 9)),
    Member(id=5, member_number="MEM-0005", full_name="Njeri Wambui", email="njeri.wambui@example.com", phone_number="+254712345005", status=MemberStatus.ACTIVE, joined_at=_d(2024, 8, 22), created_at=_d(2024, 8, 22), updated_at=_d(2024, 8, 22)),
    Member(id=6, member_number="MEM-0006", full_name="Kiptoo Rotich", email="kiptoo.rotich@example.com", phone_number="+254712345006", status=MemberStatus.ACTIVE, joined_at=_d(2024, 10, 5), created_at=_d(2024, 10, 5), updated_at=_d(2024, 10, 5)),
    Member(id=7, member_number="MEM-0007", full_name="Adhiambo Owino", email="adhiambo.owino@example.com", phone_number="+254712345007", status=MemberStatus.SUSPENDED, joined_at=_d(2023, 6, 18), created_at=_d(2023, 6, 18), updated_at=_d(2026, 3, 1)),
    Member(id=8, member_number="MEM-0008", full_name="Mwangi Kariuki", email="mwangi.kariuki@example.com", phone_number="+254712345008", status=MemberStatus.ACTIVE, joined_at=_d(2025, 3, 30), created_at=_d(2025, 3, 30), updated_at=_d(2025, 3, 30)),
    Member(id=9, member_number="MEM-0009", full_name="Chebet Korir", email="chebet.korir@example.com", phone_number="+254712345009", status=MemberStatus.ACTIVE, joined_at=_d(2025, 7, 11), created_at=_d(2025, 7, 11), updated_at=_d(2025, 7, 11)),
    Member(id=10, member_number="MEM-0010", full_name="Wafula Simiyu", email="wafula.simiyu@example.com", phone_number="+254712345010", status=MemberStatus.ACTIVE, joined_at=_d(2025, 9, 2), created_at=_d(2025, 9, 2), updated_at=_d(2025, 9, 2)),
    Member(id=11, member_number="MEM-0011", full_name="Nyambura Githinji", email="nyambura.githinji@example.com", phone_number="+254712345011", status=MemberStatus.INACTIVE, joined_at=_d(2024, 4, 17), created_at=_d(2024, 4, 17), updated_at=_d(2025, 12, 1)),
    Member(id=12, member_number="MEM-0012", full_name="Barasa Wanyama", email="barasa.wanyama@example.com", phone_number="+254712345012", status=MemberStatus.ACTIVE, joined_at=_d(2026, 1, 20), created_at=_d(2026, 1, 20), updated_at=_d(2026, 1, 20)),
]

_next_id = 13


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
        updated = member.model_copy(update={**updates, "updated_at": datetime.now(timezone.utc)})
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
    global _members, _next_id
    _members = list(_SEED_MEMBERS)
    _next_id = 13
