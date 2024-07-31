from fastapi import APIRouter

from src.api.applications.applications_router import get_application_router
from src.api.auth.auth_controller import router as auth_router
from src.api.messangers.messangers_routers import get_messangers_router
from src.api.searches.searchings_routers import get_searching_router
from src.api.users.user_router import get_users_router


def get_apps_router():
    router = APIRouter()
    router.include_router(auth_router)
    router.include_router(get_application_router())
    router.include_router(get_messangers_router())
    router.include_router(get_searching_router())
    router.include_router(get_users_router())

    return router
