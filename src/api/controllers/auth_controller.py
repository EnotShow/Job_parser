from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from src.api.containers.services_containers.auth_service_container import AuthServiceContainer
from src.api.dtos.auth_dto import RefreshTokenDTO
from src.api.dtos.user_dto import UserCreateDTO, ChangePasswordDTO
from src.api.services.auth_service import AuthService

router = APIRouter(prefix="", tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
@inject
async def login_user(auth_service: AuthService = Depends(Provide[AuthServiceContainer.auth_service])):
    return auth_service.login("email", "password")


@router.post("/register", status_code=status.HTTP_200_OK)
@inject
async def register_user(
        dto: UserCreateDTO,
        auth_service: AuthService = Depends(Provide[AuthServiceContainer.auth_service])
):
    return await auth_service.register(dto)


@router.post("/refresh", status_code=status.HTTP_200_OK)
@inject
async def refresh_user_access_token(
        dto: RefreshTokenDTO,
        auth_service: AuthService = Depends(Provide[AuthServiceContainer.auth_service])
):
    return await auth_service.update_refresh_token(dto.token)


@router.post("/change_password", status_code=status.HTTP_200_OK, response_model=None)
@inject
async def change_user_password(
    dto: ChangePasswordDTO,
    auth_service: AuthService = Depends(Provide[AuthServiceContainer.auth_service])
):
    await auth_service.change_password(dto.old_password, dto.new_password)
    return {"message": "Password changed!"}


@router.get("/logout", status_code=status.HTTP_200_OK)
@inject
async def logout_user():
    pass
