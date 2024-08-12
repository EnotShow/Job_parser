from aiogram import types
from asyncpg import UniqueViolationError
from dependency_injector.wiring import Provide, inject
from sqlalchemy.exc import IntegrityError

from core.db.uow import UnitOfWork
from core.shared.async_session_container import UnitOfWorkContainer
from core.shared.base_service import BaseService
from core.shared.errors import NoRowsFoundError, AlreadyExistError
from src.api.middleware.dtos.pagination_dto import PaginationDTO
from src.api.users.user_dto import UserFilterDTO, UserCreateDTO, UserDTO, UserUpdateDTO, UserSelfUpdateDTO
from src.api.users.user_repository import UserRepository


class UserService(BaseService):

    @inject
    def __init__(self, uow: UnitOfWork = Provide[UnitOfWorkContainer.uow]):
        self.uow = uow

    async def get_all_users(self, limit: int = 10, page: int = 1) -> PaginationDTO[UserDTO]:
        async with self.uow as uow:
            repository = UserRepository(uow)
            try:
                response_objects = await repository.get(limit=limit, page=page)
                total = await repository.get_count(UserFilterDTO())
                return self._paginate(response_objects, page, total)
            except Exception as e:
                raise NoRowsFoundError(f"Users not found")

    async def get_user(self, user_id: int) -> UserDTO:
        async with self.uow as uow:
            repository = UserRepository(uow)
            try:
                return await repository.get_single(user_id)
            except Exception as e:
                raise NoRowsFoundError(f"User {user_id} not found")

    async def get_user_by_email(self, email: str) -> UserDTO:
        async with self.uow as uow:
            repository = UserRepository(uow)
            try:
                user_filter = UserFilterDTO(email=email)
                return await repository.get_filtered(user_filter)
            except Exception as e:
                raise NoRowsFoundError(f"User with email {email} not found")

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserDTO:
        async with self.uow as uow:
            repository = UserRepository(uow)
            try:
                user_filter = UserFilterDTO(telegram_id=telegram_id)
                return await repository.get_filtered(user_filter)
            except Exception as e:
                raise NoRowsFoundError(f"User with telegram id {telegram_id} not found")

    async def get_by_email_password(self, email: str, password: str) -> UserDTO:
        async with self.uow as uow:
            repository = UserRepository(uow)
            try:
                return await repository.get_by_email_password(email, password)
            except Exception as e:
                raise NoRowsFoundError(f"User with email {email} not found")

    async def get_user_referrals(self, refer_id: int, count: bool = False) -> [UserDTO, int]:
        async with self.uow as uow:
            repository = UserRepository(uow)
            try:
                if count:
                    return await repository.get_count(UserFilterDTO(refer_id=refer_id))
                return await repository.get_filtered(UserFilterDTO(refer_id=refer_id))
            except Exception as e:
                raise NoRowsFoundError(f"No referrals found for refer_id {refer_id}")

    async def create_user(self, user: UserCreateDTO) -> UserDTO:
        async with self.uow as uow:
            repository = UserRepository(uow)
            try:
                return await repository.create(user)
            except (IntegrityError, UniqueViolationError) as e:
                raise AlreadyExistError(f"User with this email already exists")

    async def create_user_from_telegram(self, message: types.Message, ref: str = None) -> UserDTO:
        user_data = UserCreateDTO(
            email=None,
            password=None,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            telegram_id=message.from_user.id,
            language_code=message.from_user.language_code,
            selected_language=message.from_user.language_code,
            refer_id=ref
        )
        async with self.uow as uow:
            repository = UserRepository(uow)
            return await repository.create(user_data)

    async def update_user(self, user: UserUpdateDTO, user_id: int) -> UserDTO:
        async with self.uow as uow:
            repository = UserRepository(uow)
            try:
                user.id = user_id
                return await repository.update(user)
            except Exception as e:
                raise e

    async def update_self(self, user: UserSelfUpdateDTO, user_id: int) -> UserDTO:
        try:
            user.id = user_id
            user = UserUpdateDTO(**user.dict())
            return await self.update_user(user, user_id=user.id)
        except Exception as e:
            raise e

    async def get_user_settings(self, user_id: int) -> UserDTO:
        async with self.uow as uow:
            repository = UserRepository(uow)
            try:
                return await repository.get_user_settings(user_id)
            except Exception as e:
                raise e

    async def delete_user(self, user_id: int):
        async with self.uow as uow:
            repository = UserRepository(uow)
            try:
                await repository.delete(user_id)
            except Exception as e:
                raise e
