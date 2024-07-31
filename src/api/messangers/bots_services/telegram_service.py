from typing import List

from bot_create import bot
from src.api.messangers.dtos.notification_dto import NotificationDTO


class TelegramService:

    def __init__(self, bot=bot):
        self._bot = bot
        self._repository = None

    async def send_notification(self, notification_dto: NotificationDTO):
        await self._bot.send_message(notification_dto.social_network_id, notification_dto.message)

    async def send_multiple_notifications(self, notifications_dto: List[NotificationDTO]):
        for notification_dto in notifications_dto:
            await self.send_notification(notification_dto)
