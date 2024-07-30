from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import IntegrityError

from core.shared.base_service import BaseService
from core.shared.errors import AlreadyExistError
from src.api.containers.services_containers.user_service_container import UserServiceContainer
from src.api.dtos.auth_dto import TokenDTO, RefreshTokenDTO, AccessTokenDTO
from src.api.dtos.user_dto import UserCreateDTO, UserRegisterDTO, UserUpdateDTO, UserFilterDTO
from src.api.services.jwt_service import jwt_service, JwtService
from src.api.services.user_service import UserService


class AuthService(BaseService):
    @inject
    def __init__(self, jwt_service: JwtService = jwt_service,
                 user_service: UserService = Provide[UserServiceContainer.user_service]):
        self._user_service = user_service
        self._jwt_service = jwt_service

    async def login(self, email: str, password: str) -> TokenDTO:
        password = await self._jwt_service.encode_password(password)
        user = await self._user_service.get_by_email_password(email, password)
        if user:
            return await self._jwt_service.create_tokens(user)

    async def refresh_access_token(self, refresh_token: str) -> AccessTokenDTO:
        data = await self._jwt_service.decode_token(refresh_token)
        user = await self._user_service.get_user(int(data['user']["user_id"]))
        return await self._jwt_service.generate_access_token(user)

    async def register(self, user: UserRegisterDTO) -> TokenDTO:
        user = UserCreateDTO(**user.dict())
        user.selected_language = user.language_code
        user.password = await self._jwt_service.encode_password(user.password)
        try:
            user = await self._user_service.create_user(user)
        except AlreadyExistError:
            raise AlreadyExistError("User with this email already exists")
        return await self._jwt_service.create_tokens(user)

    async def change_password(
            self,
            user_email,
            old_password: str,
            new_password: str,
    ) -> TokenDTO:
        old_password_encoded = await self._jwt_service.encode_password(old_password)
        new_password = await self._jwt_service.encode_password(new_password)
        user = await self._user_service.get_by_email_password(user_email, old_password_encoded)
        user_dto = UserUpdateDTO(id=user.id, password=new_password)
        user = await self._user_service.update_user(user_dto)
        return await self._jwt_service.create_tokens(user)
