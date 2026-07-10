from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.repositories.factory import get_member_repository, get_shares_repository
from app.schemas.common import ApiResponse, PaginatedData
from app.schemas.shares import PurchaseSharesRequest, ShareAccountOut
from app.services.shares_service import MemberNotFoundForSharesError, SharesService

router = APIRouter(prefix="/shares", tags=["Shares"])


def get_shares_service() -> SharesService:
    return SharesService(
        shares_repository=get_shares_repository(),
        member_repository=get_member_repository(),
    )


@router.get("", response_model=ApiResponse[PaginatedData[ShareAccountOut]])
async def list_share_accounts(
    member_id: int | None = Query(default=None),
    shares_service: SharesService = Depends(get_shares_service),
):
    accounts = await shares_service.list_accounts(member_id)

    return ApiResponse(
        success=True,
        message="Share accounts retrieved",
        data=PaginatedData(
            items=[ShareAccountOut.model_validate(a) for a in accounts],
            page=1,
            page_size=len(accounts) or 1,
            total_items=len(accounts),
            total_pages=1,
        ),
    )


@router.post("/purchase", response_model=ApiResponse[ShareAccountOut], status_code=status.HTTP_201_CREATED)
async def purchase_shares(
    payload: PurchaseSharesRequest, shares_service: SharesService = Depends(get_shares_service)
):
    try:
        account = await shares_service.purchase(payload.member_id, payload.number_of_shares)
    except MemberNotFoundForSharesError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ApiResponse(
        success=True, message="Shares purchased", data=ShareAccountOut.model_validate(account)
    )
