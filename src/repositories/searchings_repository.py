from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError

from core.shared.repository_dependencies import IAsyncSession
from src.dtos.search_dto import SearchCreateDTO, SearchDTO
from src.models.search import Search


class SearchRepository:
    model = Search

    def __init__(self, db_session: IAsyncSession):
        self._session = db_session

    async def get_all(self):
        stmt = select(self.model)
        try:
            result = await self._session.execute(stmt)
            rows = result.scalars().all()
            return [self._get_dto(row) for row in rows]
        except (NoResultFound, AttributeError):
            return None

    async def create(self, dto: SearchCreateDTO):
        instance = self.model(**dto.model_dump())
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError as e:
            raise Exception(str(e))
        await self._session.refresh(instance)
        return self._get_dto(instance)

    def _get_dto(self, row):
        return SearchDTO(**row.__dict__)
