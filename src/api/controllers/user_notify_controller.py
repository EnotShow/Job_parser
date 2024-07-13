from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from src.api.containers.bots_containers.notification_container import NotificationServiceContainer
from src.api.dtos.notification_dto import NotificationDTO
from src.api.services.bots_services.notification_service import NotificationService

router = APIRouter(prefix="/notify", tags=["notifications"])


@router.post("/notify", status_code=status.HTTP_200_OK)
@inject
async def send_notifications(
        data: NotificationDTO,
        notification_service: NotificationService = Depends(Provide[NotificationServiceContainer.notification_service]),
):
    try:
        return await notification_service.send_notification(data.notification)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'Unexpected error'})


@router.post("/notify_multiple", status_code=status.HTTP_200_OK)
@inject
async def send_multiple_notifications(
        data: List[NotificationDTO],
        notification_service: NotificationService = Depends(Provide[NotificationServiceContainer.notification_service]),
):
    try:
        return await notification_service.send_multiple_notifications(data)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'Unexpected error'})
