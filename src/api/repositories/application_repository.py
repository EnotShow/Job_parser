from typing import AsyncContextManager, List

from dependency_injector.wiring import Provide, inject
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.shared.async_session_container import AsyncSessionContainer
from core.shared.base_repository import BaseRepository
from core.shared.errors import NoRowsFoundError
from src.api.dtos.application_dto import ApplicationDTO, ApplicationCreateDTO, ApplicationFilterDTO, \
    ApplicationUpdateDTO
from src.api.models import Application


class ApplicationRepository(BaseRepository):
    model = Application

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

    async def get_single(self, id: int) -> ApplicationDTO:
        stmt = select(self.model).where(self.model.id == id)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            return None

    async def get_filtered(self, filters: ApplicationFilterDTO, get_single: bool = False, count: bool = False
                           ) -> [List[ApplicationDTO], ApplicationDTO, int]:
        stmt = select(self.model).where(*filters.to_orm_expressions(self.model))
        try:
            result = await self._session.execute(stmt)
            if get_single:
                if count:
                    raise Exception("Single object can't be counted")
                row = result.scalars().first()
                return self._get_dto(row)
            if count:
                return result.scalars().all().count(self.model)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise Exception(f"Application objects not found")

    async def get_by_url(self, url: str) -> ApplicationDTO:
        stmt = select(self.model).where(self.model.url == url)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            return None

    async def create(self, dto: ApplicationCreateDTO):
        instance = self.model(**dto.model_dump())
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError as e:
            raise Exception(str(e))
        await self._session.refresh(instance)
        return self._get_dto(instance)

    async def create_multiple(self, dtos: [ApplicationCreateDTO]):
        for dto in dtos:
            instance = self.model(**dto.model_dump())
            self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError as e:
            raise Exception(str(e))

    async def update(self, dto: ApplicationUpdateDTO):
        stmt = update(self.model).where(self.model.id == dto.id).values(**dto.to_orm_values()).returning(self.model)
        result = await self._session.execute(stmt)
        await self._session.commit()
        try:
            return self._get_dto(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} no found")
        
    async def delete(self, id: int):
        stmt = delete(self.model).where(self.model.id == id)
        res = await self._session.execute(stmt)
        if res.rowcount == 0:
            raise NoResultFound(f"{self.model.__name__} not found")
        await self._session.commit()

    def _get_dto(self, row):
        return ApplicationDTO(**row.__dict__)
