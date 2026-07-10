from datetime import datetime, timezone

from app.models.contribution import Contribution, ContributionType
from app.repositories.mock.contribution_repository import MockContributionRepository
from app.repositories.mock.member_repository import MockMemberRepository


class MemberNotFoundForContributionError(Exception):
    pass


class ContributionService:
    def __init__(
        self,
        contribution_repository: MockContributionRepository,
        member_repository: MockMemberRepository,
    ):
        self._contribution_repository = contribution_repository
        self._member_repository = member_repository

    async def list_contributions(
        self, member_id: int | None, contribution_type: ContributionType | None
    ) -> list[Contribution]:
        return await self._contribution_repository.filter(member_id, contribution_type)

    async def record(
        self, member_id: int, contribution_type: ContributionType, amount: float
    ) -> Contribution:
        member = await self._member_repository.get_by_id(member_id)
        if member is None:
            raise MemberNotFoundForContributionError(f"Member with id {member_id} does not exist")

        now = datetime.now(timezone.utc)
        new_contribution = Contribution(
            id=0,  # overwritten by repository
            member_id=member_id,
            type=contribution_type,
            amount=amount,
            contributed_at=now,
            created_at=now,
        )
        return await self._contribution_repository.create(new_contribution)
