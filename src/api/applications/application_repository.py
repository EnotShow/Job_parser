from operator import or_
from typing import List

from sqlalchemy import select, update, delete, and_, func
from sqlalchemy.exc import NoResultFound, IntegrityError

from core.db.uow import UnitOfWork
from core.shared.base_repository import BaseRepository
from core.shared.errors import NoRowsFoundError
from src.api.applications.application_dto import ApplicationDTO, ApplicationCreateDTO, ApplicationFilterDTO, \
    ApplicationUpdateDTO, ApplicationFullDTO
from src.api.applications.application_model import Application


class ApplicationRepository(BaseRepository):
    model = Application

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def get(self, limit: int = 10, page: int = 1) -> List[ApplicationDTO]:
        offset = (page - 1) * limit
        stmt = select(self.model).limit(limit).offset(offset)
        try:
            result = await self._uow.session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise NoRowsFoundError(f"{self.model.__name__} not found")

    async def get_single(self, id: int) -> ApplicationDTO:
        stmt = select(self.model).where(self.model.id == id)
        try:
            result = await self._uow.session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            raise NoRowsFoundError(f"{self.model.__name__} not found")

    async def get_filtered(self, filters: ApplicationFilterDTO, *, limit: int = 10, page: int = 1) -> List[ApplicationDTO]:
        offset = (page - 1) * limit
        stmt = select(self.model).where(*filters.to_orm_expressions(self.model)).limit(limit).offset(offset)
        try:
            result = await self._uow.session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise NoRowsFoundError(f"{self.model.__name__} not found")

    async def get_count(self, filters: ApplicationFilterDTO) -> int:
        try:
            stmt = select(func.count(self.model.id)).where(*filters.to_orm_expressions(self.model))
            result = await self._uow.session.execute(stmt)
            count = result.scalars().first()
            return count
        except Exception as e:
            raise Exception(str(e))

    async def get_filtered_multiple_applications(self, filters: List[ApplicationFilterDTO], *, limit: int = 10, page: int = 1):
        def recursive_or_conditions(filters: List[ApplicationFilterDTO]):
            if len(filters) == 1:
                or_condition = and_(Application.url == filters[0].url, Application.owner_id == filters[0].owner_id)
                return or_condition
            else:
                or_condition = and_(Application.url == filters[-1].url, Application.owner_id == filters[-1].owner_id)
                filters.pop()
                return or_(or_condition, recursive_or_conditions(filters))

        offset = (page - 1) * limit
        or_conditions = recursive_or_conditions(filters)
        stmt = select(self.model).where(or_conditions).limit(limit).offset(offset)
        try:
            result = await self._uow.session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError) as e:
            raise NoRowsFoundError(f"{self.model.__name__} not found")

    async def get_by_url(self, url: str) -> ApplicationDTO:
        stmt = select(self.model).where(self.model.url == url)
        try:
            result = await self._uow.session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            raise NoRowsFoundError(f"{self.model.__name__} not found")

    async def create(self, dto: ApplicationCreateDTO):
        instance = self.model(**dto.model_dump())
        self._uow.session.add(instance)
        try:
            await self._uow.commit()
            await self._uow.session.refresh(instance)
            return self._get_full_dto(instance)
        except IntegrityError as e:
            await self._uow.rollback()
            raise Exception(str(e))

    async def create_multiple(self, dtos: List[ApplicationCreateDTO]) -> List[ApplicationFullDTO]:
        created_instances = []
        for dto in dtos:
            instance = self.model(**dto.model_dump())
            self._uow.session.add(instance)
            created_instances.append(instance)
        try:
            await self._uow.commit()
            for instance in created_instances:
                await self._uow.session.refresh(instance)
            return [self._get_full_dto(instance) for instance in created_instances]
        except IntegrityError as e:
            await self._uow.rollback()
            raise Exception(str(e))

    async def update(self, dto: ApplicationUpdateDTO):
        stmt = update(self.model).where(self.model.id == dto.id).values(**dto.to_orm_values()).returning(self.model)
        result = await self._uow.session.execute(stmt)
        await self._uow.commit()
        try:
            return self._get_dto(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} not found")

    async def delete(self, id: int):
        stmt = delete(self.model).where(self.model.id == id)
        res = await self._uow.session.execute(stmt)
        if res.rowcount == 0:
            raise NoResultFound(f"{self.model.__name__} not found")
        await self._uow.commit()

    def _get_dto(self, row):
        return ApplicationDTO(**row.__dict__)

    def _get_full_dto(self, row):
        return ApplicationFullDTO(**row.__dict__)
