from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.models.contribution import ContributionType
from app.repositories.factory import get_contribution_repository, get_member_repository
from app.schemas.common import ApiResponse, PaginatedData
from app.schemas.contribution import ContributionOut, RecordContributionRequest
from app.services.contribution_service import ContributionService, MemberNotFoundForContributionError

router = APIRouter(prefix="/contributions", tags=["Contributions"])


def get_contribution_service() -> ContributionService:
    return ContributionService(
        contribution_repository=get_contribution_repository(),
        member_repository=get_member_repository(),
    )


@router.get("", response_model=ApiResponse[PaginatedData[ContributionOut]])
async def list_contributions(
    member_id: int | None = Query(default=None),
    type_filter: ContributionType | None = Query(default=None, alias="type"),
    contribution_service: ContributionService = Depends(get_contribution_service),
):
    contributions = await contribution_service.list_contributions(member_id, type_filter)

    return ApiResponse(
        success=True,
        message="Contributions retrieved",
        data=PaginatedData(
            items=[ContributionOut.model_validate(c) for c in contributions],
            page=1,
            page_size=len(contributions) or 1,
            total_items=len(contributions),
            total_pages=1,
        ),
    )


@router.post("", response_model=ApiResponse[ContributionOut], status_code=status.HTTP_201_CREATED)
async def record_contribution(
    payload: RecordContributionRequest,
    contribution_service: ContributionService = Depends(get_contribution_service),
):
    try:
        contribution = await contribution_service.record(
            payload.member_id, payload.type, payload.amount
        )
    except MemberNotFoundForContributionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ApiResponse(
        success=True, message="Contribution recorded", data=ContributionOut.model_validate(contribution)
    )
