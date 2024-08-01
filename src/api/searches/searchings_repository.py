from typing import List

from dependency_injector.wiring import Provide, inject
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.shared.async_session_container import AsyncSessionContainer
from core.shared.base_repository import BaseRepository
from core.shared.errors import NoRowsFoundError
from src.api.searches.search_dto import SearchCreateDTO, SearchDTO, SearchFilterDTO, SearchUpdateDTO
from src.api.searches.search_model import Search


class SearchRepository(BaseRepository):
    model = Search

    @inject
    def __init__(self, db_session: AsyncSession = Provide[AsyncSessionContainer.db_session]) -> None:
        self._session = db_session

    async def get(self, limit: int = 10, page: int = 1) -> list[SearchDTO]:
        offset = (page - 1) * limit
        stmt = select(self.model).limit(limit).offset(offset)
        try:
            result = await self._session.execute(stmt)
            rows = result.scalars().all()
            return[self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise NoRowsFoundError(f"{self.model.__name__} no found")

    async def get_single(self, id: int) -> SearchDTO:
        stmt = select(self.model).where(self.model.id == id)
        try:
            result = await self._session.execute(stmt)
            return self._get_dto(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} no found")

    async def get_filtered(self, filters: SearchFilterDTO, *,
                           limit: int = 10, page: int = 1, count: bool = False) -> [List[SearchDTO], SearchDTO, int]:
        offset = (page - 1) * limit
        stmt = select(self.model).where(*filters.to_orm_expressions(self.model))
        if not count:
            stmt.limit(limit).offset(offset)
        try:
            result = await self._session.execute(stmt)
            if count:
                return result.scalars().all().count(self.model)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise Exception(f"Search objects not found")

    async def create(self, dto: SearchCreateDTO):
        instance = self.model(**dto.model_dump())
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError as e:
            raise Exception(str(e))
        await self._session.refresh(instance)
        return self._get_dto(instance)

    async def update(self, dto: SearchUpdateDTO) -> SearchDTO:
        stmt = (update(self.model)
                .where(self.model.id == dto.id)
                .values(**dto.to_orm_values())
                .returning(self.model))
        result = await self._session.execute(stmt)
        await self._session.commit()
        try:
            return SearchDTO.model_validate(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} no found")

    async def delete(self, id: int):
        stmt = delete(self.model).where(self.model.id == id)
        res = await self._session.execute(stmt)
        if res.rowcount == 0:
            raise NoResultFound(f"{self.model.__name__} not found")
        await self._session.commit()

    def _get_dto(self, row):
        return SearchDTO(**row.__dict__)
