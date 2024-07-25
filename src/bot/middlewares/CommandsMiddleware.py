from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class CommandsMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        if event.text.startswith('/'):
            bot_commands = await event.bot.get_my_commands()
            bot_commands = [x.command for x in bot_commands]
            if event.text[1:] in bot_commands and data["state"]:
                await data["state"].clear()
        return await handler(event, data)
