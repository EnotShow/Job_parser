from fastapi import APIRouter

from src.api.users.controllers.user_controller import router as user_router
from src.api.users.controllers.user_service_controllers import router as user_service_router


def get_users_router():
    router = APIRouter(prefix="/users", tags=["Users"])
    router.include_router(user_router)
    router.include_router(user_service_router)

    return router
