from aiogram import types
from dependency_injector.wiring import Provide, inject

from core.shared.base_service import BaseService
from core.shared.errors import NoRowsFoundError
from src.api.containers.repositories_containers.user_repository_container import UserRepositoryContainer
from src.api.dtos.pagination_dto import PaginationDTO
from src.api.dtos.user_dto import UserFilterDTO, UserCreateDTO, UserDTO, UserUpdateDTO
from src.api.repositories.user_repository import UserRepository


class UserService(BaseService):

    @inject
    def __init__(self, repository: UserRepository = Provide[UserRepositoryContainer.user_repository]):
        self._repository = repository

    async def get_all_users(self, limit: int = 10, page: int = 1) -> PaginationDTO[UserDTO]:
        response_objects = await self._repository.get(limit=limit, page=page)
        return self._paginate(response_objects, page, len(response_objects))

    async def get_user(self, user_id: int) -> UserDTO:
        try:
            return await self._repository.get_single(user_id)
        except Exception as e:
            raise NoRowsFoundError(f"User {user_id} not found")

    async def get_user_by_email(self, email: str) -> UserDTO:
        try:
            user_filter = UserFilterDTO(email=email)
            return await self._repository.get_filtered(user_filter)
        except Exception as e:
            raise NoRowsFoundError(f"User with email {email} not found")

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserDTO:
        try:
            user_filter = UserFilterDTO(telegram_id=telegram_id)
            return await self._repository.get_filtered(user_filter)
        except Exception as e:
            raise NoRowsFoundError(f"User with telegram id {telegram_id} not found")

    async def get_by_email_password(self, email: str, password: str) -> UserDTO:
        try:
            return await self._repository.get_by_email_password(email, password)
        except Exception as e:
            raise NoRowsFoundError(f"User with email {email} not found")

    async def get_user_referrals(self, refer_id: int, count: bool = False) -> [UserDTO, int]:
        try:
            if count:
                return len(await self._repository.get_filtered(UserFilterDTO(refer_id=refer_id), count=count))
            return await self._repository.get_filtered(UserFilterDTO(refer_id=refer_id))
        except Exception as e:
            return NoRowsFoundError

    async def create_user(self, user: UserCreateDTO) -> UserDTO:
        try:
            return await self._repository.create(user)
        except Exception as e:
            raise e

    async def create_user_from_telegram(self, message: types.Message, ref: str = None) -> UserDTO:
        user_data = UserCreateDTO(
            email=None,
            password=None,
            telegram_id=message.from_user.id,
            language_code=message.from_user.language_code,
            selected_language=message.from_user.language_code,
            refer_id=ref
        )
        return await self._repository.create(user_data)

    async def update_user(self, user: UserUpdateDTO) -> UserDTO:
        try:
            return await self._repository.update(user)
        except Exception as e:
            raise e

    async def get_user_settings(self, user_id: int) -> UserDTO:
        try:
            return await self._repository.get_user_settings(user_id)
        except Exception as e:
            raise e
