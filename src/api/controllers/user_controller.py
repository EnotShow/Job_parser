from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsAuthenticated, IsService
from src.api.containers.services_containers.user_service_container import UserServiceContainer
from src.api.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/settings/{user_id}", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated, IsService])
@inject
async def get_user_settings(
        user_id: int,
        request: Request,
        user_service: UserService = Depends(Provide[UserServiceContainer.user_service]),
):
    try:
        return await user_service.get_user_settings(user_id)
    except Exception as ex:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ex))
