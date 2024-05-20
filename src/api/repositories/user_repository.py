from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound, IntegrityError

from core.shared.errors import NoRowsFoundError
from src.api.models import User

from core.shared.repository_dependencies import IAsyncSession
from src.api.dtos.user_dto import UserCreateDTO, UserDTO


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
            raise Exception(f"User with email {email} not found")

    async def get_by_email_password(self, email: str, password: str) -> UserDTO:
        stmt = select(self.model).where(self.model.email == email, self.model.password == password)
        try:
            result = await self._session.execute(stmt)
            row = result.scalars().first()
            return self._get_dto(row)
        except (NoResultFound, AttributeError):
            raise Exception(f"User with email {email} not found")

    async def create(self, dto: UserCreateDTO):
        instance = self.model(**dto.model_dump())
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError as e:
            raise Exception(str(e))
        await self._session.refresh(instance)
        return self._get_dto(instance)
    
    async def update(self, dto: UserDTO, filters: dict):
        stmt = update(self.model).filter_by(**filters).values(**dto.model_dump()).returning(self.model)
        result = await self._session.execute(stmt)
        await self._session.commit()
        try:
            return self._get_dto(result.scalar_one())
        except NoResultFound:
            raise NoRowsFoundError(f"{self.model.__name__} no found")

    def _get_dto(self, row):
        return UserDTO(**row.__dict__)
