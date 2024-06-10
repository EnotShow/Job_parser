from typing import AsyncContextManager, List

from dependency_injector.wiring import Provide, inject
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.shared.async_session_container import AsyncSessionContainer
from core.shared.base_repository import BaseRepository
from core.shared.errors import NoRowsFoundError
from src.api.dtos.search_dto import SearchCreateDTO, SearchDTO, SearchFilterDTO, SearchUpdateDTO
from src.api.models import Search


class SearchRepository(BaseRepository):
    model = Search

    @inject
    def __init__(self, db_session: AsyncSession = Provide[AsyncSessionContainer.db_session]) -> None:
        self._session = db_session

    async def get(self) -> list[SearchDTO]:
        stmt = select(self.model)
        try:
            result = await self._session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise NoRowsFoundError(f"{self.model.__name__} no found")

    async def get_single(self, id: int) -> SearchDTO:
        stmt = select(self.model).where(self.model.id == id)
        try:
            result = await self._session.execute(stmt)
            return self._get_dto(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} no found")

    async def get_filtered(self, filters: SearchFilterDTO, get_single: bool = False) -> [List[SearchDTO], SearchDTO]:
        stmt = select(self.model).where(*filters.to_orm_expressions(self.model))
        try:
            result = await self._session.execute(stmt)
            if get_single:
                row = result.scalars().first()
                return self._get_dto(row)
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
        print(dto.to_orm_expressions(self.model))
        stmt = (update(self.model)
                .where(self.model.id == dto.id)
                .values(**dto.to_orm_values())
                .returning(self.model))
        result = await self._session.execute(stmt)
        print(result)
        await self._session.commit()
        # try:
        return SearchDTO.model_validate(result.scalar_one())
        # except NoResultFound:
        #     raise NoRowsFoundError(f"{self.model.__name__} no found")

    async def delete(self, id: int):
        stmt = delete(self.model).where(self.model.id == id)
        res = await self._session.execute(stmt)
        if res.rowcount == 0:
            raise NoResultFound(f"{self.model.__name__} not found")
        await self._session.commit()

    def _get_dto(self, row):
        return SearchDTO(**row.__dict__)
