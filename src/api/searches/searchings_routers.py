from fastapi import APIRouter

from src.api.searches.controllers.searches_controllers import router as searching_router
from src.api.searches.controllers.searches_service_controllers import router as searching_service_router


def get_searching_router():
    router = APIRouter(prefix="/searches", tags=["Searches"])
    router.include_router(searching_router)
    router.include_router(searching_service_router)

    return router
