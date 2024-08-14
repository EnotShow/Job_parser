from aredis_om import NotFoundError
from dependency_injector.wiring import inject, Provide

from core.shared.base_service import BaseService
from core.shared.errors import AlreadyExistError
from src.api.auth.auth_dto import TokenDTO, AccessTokenDTO, UserRegisterDTO, AuthHashDTO
from src.api.auth.auth_repository import AuthHashRepository
from src.api.auth.containers.auth_hash_container import AuthHashRepositoryContainer
from src.api.auth.services.jwt_service import JwtService, jwt_service
from src.api.users.containers.user_service_container import UserServiceContainer
from src.api.users.user_dto import UserCreateDTO, UserUpdateDTO
from src.api.users.user_service import UserService


class AuthService(BaseService):
    @inject
    def __init__(
            self,
            jwt_service: JwtService = jwt_service,
            user_service: UserService = Provide[UserServiceContainer.user_service],
            auth_hash_repository: AuthHashRepository = Provide[AuthHashRepositoryContainer.auth_hash_repository],
    ):
        self._auth_hash_repository = auth_hash_repository
        self._user_service = user_service
        self._jwt_service = jwt_service

    async def login(self, email: str, password: str) -> TokenDTO:
        password = await self._jwt_service.encode_password(password)
        user = await self._user_service.get_by_email_password(email, password)
        if user:
            return await self._jwt_service.create_tokens(user)

    async def refresh_access_token(self, refresh_token: str) -> AccessTokenDTO:
        data = await self._jwt_service.decode_token(refresh_token)
        if data.token_type != "refresh":
            raise Exception("Invalid token type")
        user = await self._user_service.get_user(data.user.id)
        return await self._jwt_service.generate_access_token(user)

    async def verify_access_token(self, access_token: str):
        data = await self._jwt_service.decode_token(access_token)
        if data.token_type != "access":
            raise Exception("Invalid token type")
        return {"message": "Access token is valid!"}

    async def register(self, user: UserRegisterDTO) -> TokenDTO:
        user = UserCreateDTO(**user.dict())
        user.selected_language = user.language_code
        user.password = await self._jwt_service.encode_password(user.password)
        try:
            if not await self._user_service.get_user_by_email(user.email):
                user = await self._user_service.create_user(user)
                return await self._jwt_service.create_tokens(user)
            raise AlreadyExistError("User with this email already exists")
        except AlreadyExistError:
            raise AlreadyExistError("User with this email already exists")

    async def generate_login_hash(self, user_id: int) -> AuthHashDTO:
        _hash = await self._auth_hash_repository.create(AuthHashDTO(user_id=user_id))
        return _hash

    async def auth_by_auth_hash(self, _hash: str) -> TokenDTO:
        try:
            auth_hash = await self._auth_hash_repository.get(_hash)
            if auth_hash:
                user = await self._user_service.get_user(auth_hash.user_id)
                return await self._jwt_service.create_tokens(user)
        except NotFoundError:
            raise NotFoundError("Auth hash not found")

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
        user = await self._user_service.update_user(user_dto, user.id)
        return await self._jwt_service.create_tokens(user)
