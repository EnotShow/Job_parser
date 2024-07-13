from fastapi import APIRouter

from src.api.controllers.application_controller import router as application_router
from src.api.controllers.user_notify_controller import router as notification_router


def get_apps_router():
    router = APIRouter()
    router.include_router(application_router)
    router.include_router(notification_router)
    return router
