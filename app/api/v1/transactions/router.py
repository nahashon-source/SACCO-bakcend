from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.models.transaction import TransactionStatus, TransactionType
from app.repositories.factory import get_transaction_repository
from app.schemas.common import ApiResponse, PaginatedData
from app.schemas.transaction import TransactionOut
from app.services.transaction_service import TransactionNotFoundError, TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_transaction_service() -> TransactionService:
    return TransactionService(transaction_repository=get_transaction_repository())


@router.get("", response_model=ApiResponse[PaginatedData[TransactionOut]])
async def list_transactions(
    member_id: int | None = Query(default=None),
    type_filter: TransactionType | None = Query(default=None, alias="type"),
    status_filter: TransactionStatus | None = Query(default=None, alias="status"),
    transaction_service: TransactionService = Depends(get_transaction_service),
):
    transactions = await transaction_service.list_transactions(member_id, type_filter, status_filter)

    return ApiResponse(
        success=True,
        message="Transactions retrieved",
        data=PaginatedData(
            items=[TransactionOut.model_validate(t) for t in transactions],
            page=1,
            page_size=len(transactions) or 1,
            total_items=len(transactions),
            total_pages=1,
        ),
    )


@router.get("/{transaction_id}", response_model=ApiResponse[TransactionOut])
async def get_transaction(
    transaction_id: int, transaction_service: TransactionService = Depends(get_transaction_service)
):
    try:
        transaction = await transaction_service.get_transaction(transaction_id)
    except TransactionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ApiResponse(
        success=True, message="Transaction retrieved", data=TransactionOut.model_validate(transaction)
    )
