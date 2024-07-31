from fastapi import APIRouter

from src.api.messangers.user_notify_controller import router as notification_router


def get_messangers_router():
    router = APIRouter()
    router.include_router(notification_router)

    return router
