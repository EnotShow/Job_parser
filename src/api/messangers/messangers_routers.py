from fastapi import APIRouter

from src.api.messangers.bots_controllers.user_notify_controller import router as notification_router
from src.api.messangers.bots_controllers.telegram_controller import router as telegram_router


def get_messangers_router():
    router = APIRouter()
    router.include_router(notification_router)
    router.include_router(telegram_router)

    return router
