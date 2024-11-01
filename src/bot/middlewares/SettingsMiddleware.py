from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from dependency_injector.wiring import Provide

from src.api.users.containers.user_service_container import UserServiceContainer
from src.api.users.user_service import UserService


class SettingsMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
            user_service: UserService = Provide[UserServiceContainer.user_service],
    ) -> Any:
        try:
            settings = await user_service.get_user_settings_telegram(event.from_user.id)
        except Exception as e:
            settings = None
        data['settings'] = settings if settings else None
        return await handler(event, data)
