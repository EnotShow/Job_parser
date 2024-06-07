import contextlib
from typing import AsyncContextManager

from dependency_injector.wiring import Provide, inject
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.shared.async_session_container import AsyncSessionContainer
from core.shared.base_repository import BaseRepository
from core.shared.errors import NoRowsFoundError
from src.api.models import User

from src.api.dtos.user_dto import UserCreateDTO, UserDTO


class UserRepository(BaseRepository):
    model = User

    def __init__(self, db_session: AsyncSession = Provide[AsyncSessionContainer.db_session]):
        self._session = db_session

    async def get_all(self):
        stmt = select(self.model)
        try:
            result = await self._session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            return None

    async def get_by_email(self, email: str) -> UserDTO:
        stmt = select(self.model).where(self.model.email == email)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            raise Exception(f"User with email {email} not found")

    async def get_by_email_password(self, email: str, password: str) -> UserDTO:
        stmt = select(self.model).where(self.model.email == email, self.model.password == password)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            raise Exception(f"User with email {email} not found")

    async def get_by_id(self, user_id: int) -> UserDTO:
        stmt = select(self.model).where(self.model.id == user_id)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            raise Exception(f"User with id {user_id} not found")

    async def get_by_telegram_id(self, telegram_id: int) -> UserDTO:
        stmt = select(self.model).where(self.model.telegram_id == telegram_id)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            raise Exception(f"User with telegram id {telegram_id} not found")


    async def create(self, dto: UserCreateDTO):
        instance = self.model(**dto.model_dump())
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError as e:
            raise Exception(str(e))
        await self._session.refresh(instance)
        return self._get_dto(instance)
    
    async def update(self, dto: UserDTO, filters: dict):
        stmt = update(self.model).filter_by(**filters).values(**dto.model_dump()).returning(self.model)
        result = await self._session.execute(stmt)
        await self._session.commit()
        try:
            return self._get_dto(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} no found")

    def _get_dto(self, row):
        return UserDTO(**row.__dict__)
