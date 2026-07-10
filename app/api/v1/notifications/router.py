from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.repositories.factory import get_notification_repository
from app.schemas.common import ApiResponse, PaginatedData
from app.schemas.notification import NotificationOut
from app.services.notification_service import NotificationNotFoundError, NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def get_notification_service() -> NotificationService:
    return NotificationService(notification_repository=get_notification_repository())


@router.get("", response_model=ApiResponse[PaginatedData[NotificationOut]])
async def list_notifications(
    is_read: bool | None = Query(default=None),
    notification_service: NotificationService = Depends(get_notification_service),
):
    notifications = await notification_service.list_notifications(is_read)

    return ApiResponse(
        success=True,
        message="Notifications retrieved",
        data=PaginatedData(
            items=[NotificationOut.model_validate(n) for n in notifications],
            page=1,
            page_size=len(notifications) or 1,
            total_items=len(notifications),
            total_pages=1,
        ),
    )


@router.patch("/{notification_id}/read", response_model=ApiResponse[NotificationOut])
async def mark_notification_as_read(
    notification_id: int, notification_service: NotificationService = Depends(get_notification_service)
):
    try:
        notification = await notification_service.mark_as_read(notification_id)
    except NotificationNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ApiResponse(
        success=True, message="Marked as read", data=NotificationOut.model_validate(notification)
    )


@router.patch("/read-all", response_model=ApiResponse[None])
async def mark_all_notifications_as_read(
    notification_service: NotificationService = Depends(get_notification_service),
):
    await notification_service.mark_all_as_read()
    return ApiResponse(success=True, message="All marked as read", data=None)
