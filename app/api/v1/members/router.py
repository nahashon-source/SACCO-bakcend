from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.models.member import MemberStatus
from app.repositories.factory import get_member_repository
from app.schemas.common import ApiResponse, PaginatedData
from app.schemas.member import CreateMemberRequest, MemberOut, UpdateMemberRequest
from app.services.member_service import MemberNotFoundError, MemberService

router = APIRouter(prefix="/members", tags=["Members"])


def get_member_service() -> MemberService:
    return MemberService(member_repository=get_member_repository())


@router.get("", response_model=ApiResponse[PaginatedData[MemberOut]])
async def list_members(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    status_filter: MemberStatus | None = Query(default=None, alias="status"),
    member_service: MemberService = Depends(get_member_service),
):
    items, total_items = await member_service.list_members(page, page_size, search, status_filter)

    total_pages = max(1, -(-total_items // page_size))  # ceiling division

    return ApiResponse(
        success=True,
        message="Members retrieved",
        data=PaginatedData(
            items=[MemberOut.model_validate(m) for m in items],
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
        ),
    )


@router.get("/{member_id}", response_model=ApiResponse[MemberOut])
async def get_member(member_id: int, member_service: MemberService = Depends(get_member_service)):
    try:
        member = await member_service.get_member(member_id)
    except MemberNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ApiResponse(success=True, message="Member retrieved", data=MemberOut.model_validate(member))


@router.post("", response_model=ApiResponse[MemberOut], status_code=status.HTTP_201_CREATED)
async def create_member(
    payload: CreateMemberRequest, member_service: MemberService = Depends(get_member_service)
):
    member = await member_service.create_member(
        full_name=payload.full_name,
        email=payload.email,
        phone_number=payload.phone_number,
    )

    return ApiResponse(success=True, message="Member created", data=MemberOut.model_validate(member))


@router.patch("/{member_id}", response_model=ApiResponse[MemberOut])
async def update_member(
    member_id: int,
    payload: UpdateMemberRequest,
    member_service: MemberService = Depends(get_member_service),
):
    try:
        member = await member_service.update_member(member_id, payload.model_dump())
    except MemberNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ApiResponse(success=True, message="Member updated", data=MemberOut.model_validate(member))


@router.delete("/{member_id}", response_model=ApiResponse[None])
async def delete_member(member_id: int, member_service: MemberService = Depends(get_member_service)):
    try:
        await member_service.delete_member(member_id)
    except MemberNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ApiResponse(success=True, message="Member deleted", data=None)
