from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from core.shared.errors import NoRowsFoundError
from core.shared.repository_dependencies import IAsyncSession
from src.api.dtos.application_dto import ApplicationDTO, ApplicationCreateDTO
from src.api.models import Application


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

    async def get_by_id(self, id: int) -> ApplicationDTO:
        stmt = select(self.model).where(self.model.id == id)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
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

    async def update(self, dto: ApplicationDTO):
        stmt = update(self.model).where(self.model.id == dto.id).values(**dto.model_dump()).returning(self.model)
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
