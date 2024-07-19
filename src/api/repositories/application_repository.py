from datetime import datetime
from operator import or_
from typing import List, Union

from dependency_injector.wiring import Provide, inject
from sqlalchemy import select, update, delete, and_
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

    async def get_filtered_multiple_applications(
            self,
            filters: Union[ApplicationFilterDTO,List[ApplicationFilterDTO]]
    ):
        if isinstance(filters, list) and len(filters) > 1:
            def recursive_or_conditions(filters: List[ApplicationFilterDTO]):
                if len(filters) == 1:
                    or_condition = and_(
                        Application.url == filters[0].url,
                        Application.owner_id == filters[0].owner_id
                    )
                    return or_condition
                else:
                    or_condition = and_(
                        Application.url == filters[-1].url,
                        Application.owner_id == filters[-1].owner_id
                    )
                    filters.pop()
                    return or_(or_condition, recursive_or_conditions(filters))
            or_conditions = recursive_or_conditions(filters)

            stmt = select(self.model).where(or_conditions)
        else:
            stmt = select(self.model).where(
                and_(
                    Application.url == filters.url,
                    Application.owner_id == filters.owner_id
                )
            )

        try:
            result = await self._session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError) as e:
            return str(e)

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

    async def create_multiple(self, dtos: Union[ApplicationCreateDTO, List[ApplicationCreateDTO]]):
        for dto in dtos:
            instance = self.model(**dto.model_dump())
            self._session.add(instance)
        # TODO !
        # instance = [self.model(**dtos[0].model_dump())]
        try:
            c = await self._session.commit()

            print(c)
            print("created")
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
