from fastapi import APIRouter, Depends, HTTPException, status

from app.repositories.factory import get_branch_repository
from app.schemas.branch import BranchOut, CreateBranchRequest, UpdateBranchRequest
from app.schemas.common import ApiResponse, PaginatedData

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("", response_model=ApiResponse[PaginatedData[BranchOut]])
async def list_branches(branch_repository=Depends(get_branch_repository)):
    branches = await branch_repository.list_all()

    return ApiResponse(
        success=True,
        message="Branches retrieved",
        data=PaginatedData(
            items=[BranchOut.model_validate(b) for b in branches],
            page=1,
            page_size=len(branches) or 1,
            total_items=len(branches),
            total_pages=1,
        ),
    )


@router.get("/{branch_id}", response_model=ApiResponse[BranchOut])
async def get_branch(branch_id: int, branch_repository=Depends(get_branch_repository)):
    branch = await branch_repository.get_by_id(branch_id)
    if branch is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Branch {branch_id} not found")

    return ApiResponse(success=True, message="Branch retrieved", data=BranchOut.model_validate(branch))


@router.post("", response_model=ApiResponse[BranchOut], status_code=status.HTTP_201_CREATED)
async def create_branch(payload: CreateBranchRequest, branch_repository=Depends(get_branch_repository)):
    from datetime import datetime, timezone

    from app.models.branch import Branch, BranchStatus

    now = datetime.now(timezone.utc)
    new_branch = Branch(
        id=0,
        name=payload.name,
        code=payload.code,
        address=payload.address,
        manager_member_id=payload.manager_member_id,
        status=BranchStatus.ACTIVE,
        created_at=now,
        updated_at=now,
    )

    created = await branch_repository.create(new_branch)
    return ApiResponse(success=True, message="Branch created", data=BranchOut.model_validate(created))


@router.patch("/{branch_id}", response_model=ApiResponse[BranchOut])
async def update_branch(
    branch_id: int, payload: UpdateBranchRequest, branch_repository=Depends(get_branch_repository)
):
    clean_updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    updated = await branch_repository.update(branch_id, clean_updates)

    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Branch {branch_id} not found")

    return ApiResponse(success=True, message="Branch updated", data=BranchOut.model_validate(updated))
