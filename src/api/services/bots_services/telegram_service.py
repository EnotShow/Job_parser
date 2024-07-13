from bot_create import bot
from src.api.dtos.notification_dto import NotificationDTO


class TelegramService:

    def __init__(self, bot=bot):
        self._bot = bot
        self._repository = None

    async def send_notification(self, notification_dto: NotificationDTO):
        await self._bot.send_message(notification_dto.social_network_id, notification_dto.message)
