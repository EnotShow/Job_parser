from typing import List

from asyncpg import UniqueViolationError
from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import NoResultFound, IntegrityError

from core.db.uow import UnitOfWork
from core.shared.base_repository import BaseRepository
from core.shared.errors import NoRowsFoundError, AlreadyExistError
from src.api.users.user_dto import UserCreateDTO, UserDTO, UserFilterDTO, UserUpdateDTO, UserSettingsDTO
from src.api.users.user_model import User


class UserRepository(BaseRepository):
    model = User

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def get(self, limit: int = 10, page: int = 1) -> List[UserDTO]:
        offset = (page - 1) * limit
        stmt = select(self.model).limit(limit).offset(offset)
        try:
            result = await self._uow.session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise NoRowsFoundError(f"{self.model.__name__} not found")

    async def get_by_email(self, email: str) -> UserDTO:
        stmt = select(self.model).where(self.model.email == email)
        try:
            result = await self._uow.session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            raise Exception(f"User with email {email} not found")

    async def get_by_email_password(self, email: str, password: str) -> UserDTO:
        stmt = select(self.model).where(self.model.email == email, self.model.password == password)
        try:
            result = await self._uow.session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            raise Exception(f"User with email {email} not found")

    async def get_single(self, user_id: int) -> UserDTO:
        stmt = select(self.model).where(self.model.id == user_id)
        try:
            result = await self._uow.session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            raise Exception(f"User with id {user_id} not found")

    async def get_filtered(
            self,
            filters: UserFilterDTO,
            *,
            limit: int = 10,
            page: int = 1,
    ) -> [List[UserDTO], UserDTO]:
        offset = (page - 1) * limit
        stmt = select(self.model).where(*filters.to_orm_expressions(self.model)).limit(limit).offset(offset)
        try:
            result = await self._uow.session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise Exception(f"User objects not found")

    async def get_count(self, filters: UserFilterDTO = None) -> int:
        stmt = select(func.count()).select_from(self.model)
        if filters:
            stmt = stmt.where(*filters.to_orm_expressions(self.model))
        try:
            result = await self._uow.session.execute(stmt)
            count = result.scalars().first()
            return count
        except Exception as e:
            raise Exception(str(e))

    async def create(self, dto: UserCreateDTO):
        instance = self.model(**dto.model_dump())
        self._uow.session.add(instance)
        try:
            await self._uow.session.flush()
            await self._uow.session.commit()
            await self._uow.session.refresh(instance)
            return self._get_dto(instance)
        except IntegrityError as e:
            raise e
        except UniqueViolationError as e:
            raise AlreadyExistError(f"User with this email already exists")

    async def update(self, dto: UserUpdateDTO):
        stmt = update(self.model).where(self.model.id == dto.id).values(**dto.to_orm_values()).returning(self.model)
        result = await self._uow.session.execute(stmt)
        await self._uow.session.commit()
        try:
            return self._get_dto(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} not found")

    async def get_user_settings_telegram(self, user_id: int):
        stmt = select(self.model).where(self.model.telegram_id == user_id)
        try:
            result = await self._uow.session.execute(stmt)
            row = result.scalars().first()
            raw_data = row.__dict__
            raw_data['user_id'] = raw_data['id']
            return UserSettingsDTO(**row.__dict__)
        except (NoResultFound, AttributeError) as e:
            raise Exception(f"User with id {user_id} not found")

    async def get_user_settings(self, user_id: int):
        stmt = select(self.model).where(self.model.id == user_id)
        try:
            result = await self._uow.session.execute(stmt)
            row = result.scalars().first()
            return UserSettingsDTO(**row.__dict__)
        except (NoResultFound, AttributeError) as e:
            raise Exception(f"User with id {user_id} not found")

    async def delete(self, id: int):
        stmt = delete(self.model).where(self.model.id == id)
        res = await self._uow.session.execute(stmt)
        if res.rowcount == 0:
            raise NoResultFound(f"{self.model.__name__} not found")
        await self._uow.session.commit()

    def _get_dto(self, row):
        return UserDTO(**row.__dict__)
