from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsService
from src.api.messangers.bots_containers.notification_container import NotificationServiceContainer
from src.api.messangers.dtos.notification_dto import MessangerNotificationDTO
from src.api.messangers.bots_services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("/notify", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def send_notifications(
        data: MessangerNotificationDTO,
        request: Request,
        notification_service: NotificationService = Depends(Provide[NotificationServiceContainer.notification_service]),
):
    try:
        return await notification_service.send_notification(data.notification)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'Unexpected error'})


@router.post("/notify_multiple", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def send_multiple_notifications(
        data: List[MessangerNotificationDTO],
        request: Request,
        notification_service: NotificationService = Depends(Provide[NotificationServiceContainer.notification_service]),
):
    try:
        return await notification_service.send_multiple_notifications(data)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'Unexpected error'})
