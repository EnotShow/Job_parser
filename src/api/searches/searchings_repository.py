from typing import List

from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import NoResultFound, IntegrityError

from core.db.uow import UnitOfWork
from core.shared.base_repository import BaseRepository
from core.shared.errors import NoRowsFoundError
from src.api.searches.search_dto import SearchCreateDTO, SearchDTO, SearchFilterDTO, SearchUpdateDTO
from src.api.searches.search_model import Search


class SearchRepository(BaseRepository):
    model = Search

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def get(self, limit: int = 10, page: int = 1) -> list[SearchDTO]:
        offset = (page - 1) * limit
        stmt = select(self.model).limit(limit).offset(offset)
        try:
            result = await self._uow.session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise NoRowsFoundError(f"{self.model.__name__} not found")

    async def get_single(self, id: int) -> SearchDTO:
        stmt = select(self.model).where(self.model.id == id)
        try:
            result = await self._uow.session.execute(stmt)
            return self._get_dto(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} not found")

    async def get_filtered(self, filters: SearchFilterDTO, *,
                           limit: int = 10, page: int = 1) -> [List[SearchDTO], SearchDTO, int]:
        offset = (page - 1) * limit
        stmt = select(self.model).where(*filters.to_orm_expressions(self.model)).limit(limit).offset(offset)
        try:
            result = await self._uow.session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise Exception(f"Search objects not found")

    async def get_count(self, filters: SearchFilterDTO) -> int:
        try:
            stmt = select(func.count(self.model.id)).where(*filters.to_orm_expressions(self.model))
            result = await self._uow.session.execute(stmt)
            count = result.scalars().first()
            return count
        except Exception as e:
            raise Exception(str(e))

    async def create(self, dto: SearchCreateDTO):
        instance = self.model(**dto.model_dump())
        self._uow.session.add(instance)
        try:
            await self._uow.session.commit()
            await self._uow.session.refresh(instance)
            return self._get_dto(instance)
        except IntegrityError as e:
            await self._uow.session.rollback()
            raise Exception(str(e))

    async def update(self, dto: SearchUpdateDTO) -> SearchDTO:
        stmt = (update(self.model)
                .where(self.model.id == dto.id)
                .values(**dto.to_orm_values())
                .returning(self.model))
        result = await self._uow.session.execute(stmt)
        await self._uow.session.commit()
        await self._uow.session.refresh(result.scalar_one())
        try:
            return SearchDTO.model_validate(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} not found")

    async def delete(self, id: int):
        stmt = delete(self.model).where(self.model.id == id)
        res = await self._uow.session.execute(stmt)
        if res.rowcount == 0:
            raise NoResultFound(f"{self.model.__name__} not found")
        await self._uow.session.commit()

    def _get_dto(self, row):
        return SearchDTO(**row.__dict__)
