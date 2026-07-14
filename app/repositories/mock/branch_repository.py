from datetime import datetime, timezone

from app.models.branch import Branch, BranchStatus
from app.repositories.base import BaseRepository


def _d(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc)


_branches: list[Branch] = [
    Branch(id=1, name="Head Office", code="HQ", address="Nairobi CBD, Kenya", manager_member_id=None, status=BranchStatus.ACTIVE, created_at=_d(2023, 1, 1), updated_at=_d(2023, 1, 1)),
    Branch(id=2, name="Mombasa Branch", code="MSA", address="Nkrumah Road, Mombasa", manager_member_id=6, status=BranchStatus.ACTIVE, created_at=_d(2024, 3, 1), updated_at=_d(2024, 3, 1)),
    Branch(id=3, name="Kisumu Branch", code="KSM", address="Oginga Odinga Street, Kisumu", manager_member_id=None, status=BranchStatus.ACTIVE, created_at=_d(2025, 2, 1), updated_at=_d(2025, 2, 1)),
]

_next_id = 4


class MockBranchRepository(BaseRepository[Branch]):
    async def get_by_id(self, entity_id: int) -> Branch | None:
        return next((b for b in _branches if b.id == entity_id), None)

    async def list_all(self) -> list[Branch]:
        return _branches

    async def create(self, entity: Branch) -> Branch:
        global _next_id
        entity = entity.model_copy(update={"id": _next_id})
        _next_id += 1
        _branches.append(entity)
        return entity

    async def update(self, entity_id: int, updates: dict) -> Branch | None:
        branch = await self.get_by_id(entity_id)
        if branch is None:
            return None
        updated = branch.model_copy(update={**updates, "updated_at": datetime.now(timezone.utc)})
        _branches[_branches.index(branch)] = updated
        return updated

    async def delete(self, entity_id: int) -> bool:
        branch = await self.get_by_id(entity_id)
        if branch is None:
            return False
        _branches.remove(branch)
        return True


_SEED_BRANCHES = list(_branches)


def reset_branch_data() -> None:
    global _branches, _next_id
    _branches = list(_SEED_BRANCHES)
    _next_id = 4
