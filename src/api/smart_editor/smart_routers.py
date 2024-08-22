from fastapi import APIRouter

from src.api.smart_editor.controllers.smart_controllers import router as smart_router


def get_smart_router():
    router = APIRouter(prefix="/smart-editor", tags=["SmartEditor"])
    router.include_router(smart_router)

    return router
