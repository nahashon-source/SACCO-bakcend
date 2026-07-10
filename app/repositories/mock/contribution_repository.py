from datetime import datetime, timezone

from app.models.contribution import Contribution, ContributionType
from app.repositories.base import BaseRepository


def _d(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc)


_contributions: list[Contribution] = [
    Contribution(id=1, member_id=1, type=ContributionType.MONTHLY, amount=2000, contributed_at=_d(2026, 4, 1), created_at=_d(2026, 4, 1)),
    Contribution(id=2, member_id=2, type=ContributionType.MONTHLY, amount=2000, contributed_at=_d(2026, 4, 1), created_at=_d(2026, 4, 1)),
    Contribution(id=3, member_id=1, type=ContributionType.MONTHLY, amount=2000, contributed_at=_d(2026, 5, 1), created_at=_d(2026, 5, 1)),
    Contribution(id=4, member_id=2, type=ContributionType.MONTHLY, amount=2000, contributed_at=_d(2026, 5, 1), created_at=_d(2026, 5, 1)),
    Contribution(id=5, member_id=4, type=ContributionType.MONTHLY, amount=1500, contributed_at=_d(2026, 5, 3), created_at=_d(2026, 5, 3)),
    Contribution(id=6, member_id=1, type=ContributionType.MONTHLY, amount=2000, contributed_at=_d(2026, 6, 1), created_at=_d(2026, 6, 1)),
    Contribution(id=7, member_id=2, type=ContributionType.MONTHLY, amount=2000, contributed_at=_d(2026, 6, 1), created_at=_d(2026, 6, 1)),
    Contribution(id=8, member_id=6, type=ContributionType.MONTHLY, amount=2500, contributed_at=_d(2026, 6, 2), created_at=_d(2026, 6, 2)),
    Contribution(id=9, member_id=1, type=ContributionType.WELFARE, amount=500, contributed_at=_d(2026, 6, 15), created_at=_d(2026, 6, 15)),
    Contribution(id=10, member_id=8, type=ContributionType.SPECIAL, amount=5000, contributed_at=_d(2026, 6, 20), created_at=_d(2026, 6, 20)),
    Contribution(id=11, member_id=9, type=ContributionType.MONTHLY, amount=1000, contributed_at=_d(2026, 7, 1), created_at=_d(2026, 7, 1)),
]

_next_id = 12


class MockContributionRepository(BaseRepository[Contribution]):
    async def get_by_id(self, entity_id: int) -> Contribution | None:
        return next((c for c in _contributions if c.id == entity_id), None)

    async def list_all(self) -> list[Contribution]:
        return _contributions

    async def filter(self, member_id: int | None, contribution_type: ContributionType | None) -> list[Contribution]:
        results = _contributions
        if member_id is not None:
            results = [c for c in results if c.member_id == member_id]
        if contribution_type is not None:
            results = [c for c in results if c.type == contribution_type]
        return results

    async def create(self, entity: Contribution) -> Contribution:
        global _next_id
        entity = entity.model_copy(update={"id": _next_id})
        _next_id += 1
        _contributions.append(entity)
        return entity

    async def update(self, entity_id: int, updates: dict) -> Contribution | None:
        contribution = await self.get_by_id(entity_id)
        if contribution is None:
            return None
        updated = contribution.model_copy(update=updates)
        _contributions[_contributions.index(contribution)] = updated
        return updated

    async def delete(self, entity_id: int) -> bool:
        contribution = await self.get_by_id(entity_id)
        if contribution is None:
            return False
        _contributions.remove(contribution)
        return True


_SEED_CONTRIBUTIONS = list(_contributions)


def reset_contribution_data() -> None:
    global _contributions, _next_id
    _contributions = list(_SEED_CONTRIBUTIONS)
    _next_id = 12
