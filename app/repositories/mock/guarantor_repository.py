from datetime import datetime, timezone

from app.models.guarantor import Guarantor, GuarantorStatus
from app.repositories.base import BaseRepository


def _d(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc)


_guarantors: list[Guarantor] = [
    Guarantor(id=1, loan_id=1, member_id=2, guaranteed_amount=40000, status=GuarantorStatus.ACCEPTED, responded_at=_d(2025, 1, 12), created_at=_d(2025, 1, 11), updated_at=_d(2025, 1, 12)),
    Guarantor(id=2, loan_id=2, member_id=3, guaranteed_amount=25000, status=GuarantorStatus.PENDING, responded_at=None, created_at=_d(2026, 6, 20), updated_at=_d(2026, 6, 20)),
    Guarantor(id=3, loan_id=5, member_id=1, guaranteed_amount=60000, status=GuarantorStatus.ACCEPTED, responded_at=_d(2025, 11, 15), created_at=_d(2025, 11, 13), updated_at=_d(2025, 11, 15)),
    Guarantor(id=4, loan_id=5, member_id=9, guaranteed_amount=60000, status=GuarantorStatus.ACCEPTED, responded_at=_d(2025, 11, 16), created_at=_d(2025, 11, 13), updated_at=_d(2025, 11, 16)),
    Guarantor(id=5, loan_id=6, member_id=6, guaranteed_amount=40000, status=GuarantorStatus.PENDING, responded_at=None, created_at=_d(2026, 6, 29), updated_at=_d(2026, 6, 29)),
]

_next_id = 6


class MockGuarantorRepository(BaseRepository[Guarantor]):
    async def get_by_id(self, entity_id: int) -> Guarantor | None:
        return next((g for g in _guarantors if g.id == entity_id), None)

    async def list_all(self) -> list[Guarantor]:
        return _guarantors

    async def filter(self, loan_id: int | None, member_id: int | None) -> list[Guarantor]:
        results = _guarantors
        if loan_id is not None:
            results = [g for g in results if g.loan_id == loan_id]
        if member_id is not None:
            results = [g for g in results if g.member_id == member_id]
        return results

    async def create(self, entity: Guarantor) -> Guarantor:
        global _next_id
        entity = entity.model_copy(update={"id": _next_id})
        _next_id += 1
        _guarantors.append(entity)
        return entity

    async def update(self, entity_id: int, updates: dict) -> Guarantor | None:
        guarantor = await self.get_by_id(entity_id)
        if guarantor is None:
            return None
        updated = guarantor.model_copy(update={**updates, "updated_at": datetime.now(timezone.utc)})
        _guarantors[_guarantors.index(guarantor)] = updated
        return updated

    async def delete(self, entity_id: int) -> bool:
        guarantor = await self.get_by_id(entity_id)
        if guarantor is None:
            return False
        _guarantors.remove(guarantor)
        return True


_SEED_GUARANTORS = list(_guarantors)


def reset_guarantor_data() -> None:
    global _guarantors, _next_id
    _guarantors = list(_SEED_GUARANTORS)
    _next_id = 6
