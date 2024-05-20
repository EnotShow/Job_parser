from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from core.shared.errors import NoRowsFoundError
from core.shared.repository_dependencies import IAsyncSession
from src.api.dtos.search_dto import SearchCreateDTO, SearchDTO
from src.api.models import Search


class SearchRepository:
    model = Search

    def __init__(self, db_session: IAsyncSession):
        self._session = db_session

    async def get_all(self) -> list[SearchDTO]:
        stmt = select(self.model)
        try:
            result = await self._session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            raise NoRowsFoundError(f"{self.model.__name__} no found")

    async def get(self, id: int) -> SearchDTO:
        stmt = select(self.model).where(self.model.id == id)
        try:
            result = await self._session.execute(stmt)
            return self._get_dto(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} no found")

    async def create(self, dto: SearchCreateDTO):
        instance = self.model(**dto.model_dump())
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError as e:
            raise Exception(str(e))
        await self._session.refresh(instance)
        return self._get_dto(instance)

    async def update(self, dto: SearchDTO, filters: dict) -> SearchDTO:
        stmt = update(self.model).filter_by(**filters).values(**dto.model_dump()).returning(self.model)
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
