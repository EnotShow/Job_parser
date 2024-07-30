from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request

from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsAuthenticated
from src.api.containers.services_containers.auth_service_container import AuthServiceContainer
from src.api.dtos.auth_dto import RefreshTokenDTO, AccessTokenDTO
from src.api.dtos.user_dto import ChangePasswordDTO, UserRegisterDTO, UserLoginDTO
from src.api.services.auth_service import AuthService

router = APIRouter(prefix="", tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
@inject
async def login_user(auth: UserLoginDTO, auth_service: AuthService = Depends(Provide[AuthServiceContainer.auth_service])):
    return await auth_service.login(auth.email, auth.password)


@router.post("/register", status_code=status.HTTP_200_OK)
@inject
async def register_user(
        dto: UserRegisterDTO,
        auth_service: AuthService = Depends(Provide[AuthServiceContainer.auth_service])
):
    return await auth_service.register(dto)


@router.post("/refresh", status_code=status.HTTP_200_OK)
@inject
async def refresh_user_access_token(
        dto: RefreshTokenDTO,
        auth_service: AuthService = Depends(Provide[AuthServiceContainer.auth_service])
) -> AccessTokenDTO:
    return await auth_service.refresh_access_token(dto.refresh_token)


@router.post("/change_password", status_code=status.HTTP_200_OK, response_model=None)
@permission_required([IsAuthenticated])
@inject
async def change_user_password(
    dto: ChangePasswordDTO,
    request: Request,
    auth_service: AuthService = Depends(Provide[AuthServiceContainer.auth_service])
):
    await auth_service.change_password(dto.old_password, dto.new_password)
    return {"message": "Password changed!"}


@router.get("/logout", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def logout_user():
    pass
