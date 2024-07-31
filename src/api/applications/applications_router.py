from fastapi import APIRouter

from src.api.applications.controllers.application_controller import router as application_router
from src.api.applications.controllers.service_application_controller import router as service_application_router


def get_application_router():
    router = APIRouter(prefix="/applications", tags=["Applications"])
    router.include_router(application_router)
    router.include_router(service_application_router)

    return router
