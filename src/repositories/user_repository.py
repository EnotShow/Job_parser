from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from src.models.user import User

from core.shared.repository_dependencies import IAsyncSession
from src.dtos.user_dto import UserCreateDTO, UserDTO


class UserRepository:
    model = User

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

    async def get_by_email(self, email: str) -> UserDTO:
        stmt = select(self.model).where(self.model.email == email)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            return None

    async def get_by_email_password(self, email: str, password: str) -> UserDTO:
        stmt = select(self.model).where(self.model.email == email, self.model.password == password)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            return None

    async def create(self, dto: UserCreateDTO):
        instance = self.model(**dto.model_dump())
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError as e:
            raise Exception(str(e))
        await self._session.refresh(instance)
        return self._get_dto(instance)

    def _get_dto(self, row):
        return UserDTO(**row.__dict__)