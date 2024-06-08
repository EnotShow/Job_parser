from aiogram import types
from dependency_injector.wiring import Provide, inject

from src.api.containers.repositories_containers.user_repository_container import UserRepositoryContainer
from src.api.dtos.user_dto import UserFilterDTO, UserCreateDTO, UserDTO
from src.api.repositories.user_repository import UserRepository


class UserService:

    @inject
    def __init__(self, repository: UserRepository = Provide[UserRepositoryContainer.user_repository]):
        self._repository = repository

    async def get_all_users(self):
        return await self._repository.get()

    async def get_user(self, user_id: int):
        try:
            return await self._repository.get_single(user_id)
        except Exception as e:
            return None

    async def get_user_by_email(self, email: str):
        try:
            user_filter = UserFilterDTO(email=email)
            return await self._repository.get_filtered(user_filter, get_single=False)
        except Exception as e:
            return None

    async def get_user_by_telegram_id(self, telegram_id: int):
        try:
            user_filter = UserFilterDTO(telegram_id=telegram_id)
            return await self._repository.get_filtered(user_filter, get_single=True)
        except Exception as e:
            return None

    async def get_by_email_password(self, email: str, password: str):
        try:
            # TODO password encryption
            user_filter = UserFilterDTO(email=email, password=password)
            return await self._repository.get_filtered(user_filter, get_single=True)
        except Exception as e:
            return None

    async def create_user(self, user: UserCreateDTO):
        try:
            return await self._repository.create(user)
        except Exception as e:
            return None

    async def create_user_from_telegram(self, message: types.Message):
        user_data = UserCreateDTO(
            email=None,
            password=None,
            telegram_id=message.from_user.id,
            language_code=message.from_user.language_code,
        )
        return await self._repository.create(user_data)

    async def update_user(self, user: UserDTO, filters: UserFilterDTO):
        try:
            return await self._repository.update(user, filters)
        except Exception as e:
            return None
