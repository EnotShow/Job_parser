from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, Update

from core.config.bot import settings_bot


class OwnersMiddleware(BaseMiddleware):
    def __init__(self, owners: list) -> None:
        self.owners = owners

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Update):
            if event.message.from_user.id in self.owners and event.message.chat.type == 'private':
                return await handler(event, data)
        elif isinstance(event, Message):
            if event.from_user.id in self.owners and event.chat.type == 'private':
                return await handler(event, data)