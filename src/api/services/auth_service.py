from dependency_injector.wiring import inject, Provide

from core.shared.base_service import BaseService
from src.api.containers.services_containers.user_service_container import UserServiceContainer
from src.api.dtos.auth_dto import TokenDTO, RefreshTokenDTO
from src.api.dtos.user_dto import UserCreateDTO, UserUpdateDTO
from src.api.services.jwt_service import jwt_service
from src.api.services.user_service import UserService


class AuthService(BaseService):
    @inject
    def __init__(self, jwt_service: jwt_service,
                 user_service: UserService = Provide[UserServiceContainer.user_service]):
        self._user_service = user_service
        self._jwt_service = jwt_service

    async def login(self, email: str, password: str) -> TokenDTO:
        password = await self._jwt_service.encode_password(password)
        user = await self._user_service.get_by_email_password(email, password)
        if user:
            return await self._jwt_service.generate_access_token(user)

    async def update_refresh_token(self, refresh_token: str) -> RefreshTokenDTO:
        data = await self._jwt_service.decode_token(refresh_token)
        user = await self._user_service.get_user(data["user_id"])
        return await self._jwt_service.generate_refresh_token(user)

    async def register(self, user: UserCreateDTO) -> TokenDTO:
        user.password = await self._jwt_service.encode_password(user.password)
        user = await self._user_service.create_user(user)
        return await self._jwt_service.generate_access_token(user)

    async def change_password(self, old_password: str, new_password: str) -> TokenDTO:
        pass
        # old_password_encoded = await self._jwt_service.encode_password(old_password)
        # user = await self._user_service.get_by_email_password(email=user.email, password=old_password_encoded)
        # user = await self._user_service.update_user(user_dto)
        # user_dto = UserUpdateDTO(password=password)
        # return await self._jwt_service.generate_access_token(user)