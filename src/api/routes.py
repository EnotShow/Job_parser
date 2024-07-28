from fastapi import APIRouter

from src.api.controllers.application_controller import router as application_router
from src.api.controllers.user_notify_controller import router as notification_router
from src.api.controllers.user_controller import router as user_router
from src.api.controllers.auth_controller import router as auth_router


def get_apps_router():
    router = APIRouter()
    router.include_router(auth_router)
    router.include_router(application_router)
    router.include_router(notification_router)
    user_router.include_router(router)

    return router
