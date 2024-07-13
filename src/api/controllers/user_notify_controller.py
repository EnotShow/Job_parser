from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from core.shared.enums import SocialNetworkEnum
from src.api.containers.bots_containers.telegram_container import TelegramServiceContainer
from src.api.containers.services_containers.application_service_container import ApplicationServiceContainer
from src.api.dtos.notification_dto import NotificationControllerDTO
from src.api.services.application_service import ApplicationService
from src.api.services.bots_services.telegram_service import TelegramService

router = APIRouter(prefix="/bots", tags=["bots"])


@router.post("/notify", status_code=status.HTTP_200_OK)
@inject
async def get_applications_if_exists(
        data: NotificationControllerDTO,
        telegram_service: TelegramService = Depends(Provide[TelegramServiceContainer.telegram_service]),
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service])
):
    try:
        match data.notification.social_network:
            case SocialNetworkEnum.telegram:
                await telegram_service.send_notification(data.notification)

        await application_service.create_application(data.application)
        return {'data': 'Ok'}
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'Unexpected error'})
