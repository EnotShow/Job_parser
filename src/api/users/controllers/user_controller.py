from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.requests import Request

from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsAuthenticated
from src.api.users.containers.user_service_container import UserServiceContainer
from src.api.users.user_dto import UserSelfUpdateDTO
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
        user_id = request.state.token.user.id
        user = await user_service.get_user(user_id)
        return user
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error fetching user: {str(ex)}")


@router.put("/me", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def update_me(
        data: UserSelfUpdateDTO,
        request: Request,
        user_service: UserService = Depends(Provide[UserServiceContainer.user_service]),
):
    try:
        user_id = request.state.token.user.id
        updated_user = await user_service.update_self(data, user_id)
        return updated_user
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating user: {str(ex)}")


@router.get("/me/settings", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_me_settings(
        request: Request,
        user_service: UserService = Depends(Provide[UserServiceContainer.user_service]),
):
    try:
        user_id = request.state.token.user.id
        settings = await user_service.get_user_settings(user_id)
        return settings
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error fetching user settings: {str(ex)}")
