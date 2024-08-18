from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.deep_linking import create_start_link

from bot_create import bot
from src.api.messangers.dtos.notification_dto import MessangerNotificationDTO
from src.api.messangers.dtos.telegram_dto import TelegramPayloadDTO
from src.bot.handlers.base_handlers import send_notification
from src.bot.keyboards.reply_keyboard_buttons import ReplyCallbackButtons


class TelegramService:

    def __init__(self, bot=bot):
        self._bot = bot
        self._repository = None

    async def send_notification(self, notification_dto: MessangerNotificationDTO):
        reply_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[
            ReplyCallbackButtons.button_description(
                notification_dto.application_id,
                notification_dto.search_title,
                notification_dto.language
            ),
            ReplyCallbackButtons.button_apply(
                notification_dto.application_id,
                notification_dto.search_title,
                notification_dto.language
            )
        ]])
        await send_notification(
            self._bot,
            notification_dto.social_network_id,
            notification_dto.message,
            reply_markup=reply_keyboard
        )

    async def send_multiple_notifications(self, notifications_dto: List[MessangerNotificationDTO]):
        for notification_dto in notifications_dto:
            await self.send_notification(notification_dto)

    async def encode_payload(self, payload_dto: TelegramPayloadDTO) -> dict:
        start_link = await create_start_link(
            bot=self._bot,
            payload=f"{payload_dto.model_dump(exclude_none=True)}",
            encode=True
        )
        return {"start_link": start_link}
