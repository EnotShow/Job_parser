from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError

from core.shared.repository_dependencies import IAsyncSession
from src.dtos.application_dto import ApplicationDTO, ApplicationCreateDTO
from src.models.models import Application


class ApplicationRepository:
    model = Application

    def __init__(self, db_session: IAsyncSession):
        self._session = db_session

    async def get_all(self):
        with self._session as session:
            stmt = select(self.model)
            try:
                result = await session.execute(stmt)
                rows = result.scalars().all()
                return [self._get_dto(row) for row in rows]
            except (NoResultFound, AttributeError):
                return None

    async def get_by_url(self, url: str) -> ApplicationDTO:
        stmt = select(self.model).where(self.model.url == url)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            return None

    async def create_multiple(self, dtos: [ApplicationCreateDTO]):
        for dto in dtos:
            instance = self.model(**dto.model_dump())
            self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError as e:
            raise Exception(str(e))

    def _get_dto(self, row):
        return ApplicationDTO(**row.__dict__)
