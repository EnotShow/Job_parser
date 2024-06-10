import contextlib
from typing import AsyncContextManager, List

from dependency_injector.wiring import Provide, inject
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.shared.async_session_container import AsyncSessionContainer
from core.shared.base_repository import BaseRepository
from core.shared.errors import NoRowsFoundError
from src.api.models import User

from src.api.dtos.user_dto import UserCreateDTO, UserDTO, UserFilterDTO, UserUpdateDTO


class UserRepository(BaseRepository):
    model = User

    @inject
    def __init__(self, db_session: AsyncSession = Provide[AsyncSessionContainer.db_session]):
        self._session = db_session

    async def get(self):
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

    async def get_single(self, user_id: int) -> UserDTO:
        stmt = select(self.model).where(self.model.id == user_id)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            raise Exception(f"User with id {user_id} not found")

    async def get_filtered(self, filters: UserFilterDTO, get_single: bool = False) -> [List[UserDTO], UserDTO]:
        stmt = select(self.model).where(*filters.to_orm_expressions(self.model))
        try:
            result = await self._session.execute(stmt)
            if get_single:
                row = result.scalars().first()
                return self._get_dto(row)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise Exception(f"User objects not found")

    async def create(self, dto: UserCreateDTO):
        instance = self.model(**dto.model_dump())
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError as e:
            raise Exception(str(e))
        await self._session.refresh(instance)
        return self._get_dto(instance)
    
    async def update(self, dto: UserUpdateDTO):
        stmt = update(self.model).where(self.model.id == dto.id).values(**dto.to_orm_values()).returning(self.model)
        result = await self._session.execute(stmt)
        await self._session.commit()
        try:
            return self._get_dto(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} no found")

    def _get_dto(self, row):
        return UserDTO(**row.__dict__)
