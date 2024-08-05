from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsAuthenticated, IsService
from src.api.users.containers.user_service_container import UserServiceContainer
from src.api.users.user_dto import UserUpdateDTO
from src.api.users.user_service import UserService

router = APIRouter()


@router.get("/me", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_me(
        request: Request,
        user_service: UserService = Depends(Provide[UserServiceContainer.user_service]),
):
    try:
        return await user_service.get_user(request.state.token.user.id)
    except Exception as ex:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ex))


@router.put("/me/", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def update_me(
        data: UserUpdateDTO,
        request: Request,
        user_service: UserService = Depends(Provide[UserServiceContainer.user_service]),
):
    try:
        return await user_service.update_user(data, request.state.token.user.id)
    except Exception as ex:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ex))


@router.get("/me/settings", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_me_settings(
        request: Request,
        user_service: UserService = Depends(Provide[UserServiceContainer.user_service]),
):
    try:
        return await user_service.get_user_settings(request.state.token.user.id)
    except Exception as ex:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ex))
