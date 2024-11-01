from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from core.shared.enums import SocialNetworkEnum
from src.api.messangers.bots_containers.telegram_container import TelegramServiceContainer
from src.api.messangers.dtos.notification_dto import MessangerNotificationDTO
from src.api.messangers.bots_services.telegram_service import TelegramService


class NotificationService:

    @inject
    async def send_notification(
            self,
            dto: MessangerNotificationDTO,
            telegram_service: TelegramService = Depends(Provide[TelegramServiceContainer.telegram_service])
    ):
        match dto.notification.social_network:
            case SocialNetworkEnum.telegram:
                await telegram_service.send_notification(dto)

        return {'data': 'Ok'}

    @inject
    async def send_multiple_notifications(
            self,
            dtos: List[MessangerNotificationDTO],
            telegram_service: TelegramService = Depends(Provide[TelegramServiceContainer.telegram_service])
    ):
        await telegram_service.send_multiple_notifications(dtos)
