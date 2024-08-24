from typing import List

from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import NoResultFound, IntegrityError

from core.db.uow import UnitOfWork
from core.shared.base_repository import BaseRepository
from core.shared.errors import NoRowsFoundError
from src.api.searches.search_dto import SearchCreateDTO, SearchDTO, SearchFilterDTO, SearchUpdateDTO
from src.api.searches.search_model import Search
from src.api.users.user_repository import UserRepository


class SearchRepository(BaseRepository):
    model = Search

    def __init__(
            self,
            uow: UnitOfWork
    ):
        self._uow = uow
        self._user_repository = UserRepository(uow)
        self._search_repository = SearchRepository(uow)

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
        user_settings = await self._user_repository.get_user_settings(dto.user_id)
        searches_count = await self._search_repository.get_count(SearchFilterDTO(user_id=dto.user_id))
        if searches_count >= user_settings.links_limit:
            raise Exception("User links limit reached")
        self._uow.session.add(instance)
        try:
            await self._uow.session.flush()
            await self._uow.session.commit()
            await self._uow.session.refresh(instance)
            return self._get_dto(instance)
        except IntegrityError as e:
            raise Exception(str(e))

    async def create_multiple(self, dtos: List[SearchCreateDTO]) -> List[SearchDTO]:
        created_instances = []
        users_data = {}
        # Check that all users have enough slots for links
        for dto in dtos:
            if not users_data.get(dto.user_id):
                user_settings = await self._user_repository.get_user_settings(dto.user_id)
                searches_count = await self._search_repository.get_count(SearchFilterDTO(user_id=dto.user_id))
                if searches_count >= user_settings.links_limit:
                    raise Exception(f"User links limit reached for user id: {dto.owner_id}")
                users_data[dto.user_id] = user_settings.links_limit

            # if user data links limit at least bigger than one
            if users_data[dto.user_id] - 1:
                users_data[dto.user_id] -= 1
            else:
                raise Exception(f"User links limit reached for user id: {dto.owner_id}")

        for dto in dtos:
            instance = self.model(**dto.model_dump())
            self._uow.session.add(instance)
            created_instances.append(instance)
        try:
            await self._uow.session.flush()
            await self._uow.commit()
            for instance in created_instances:
                await self._uow.session.refresh(instance)
            return [self._get_dto(instance) for instance in created_instances]
        except IntegrityError as e:
            await self._uow.rollback()
            raise Exception(str(e))

    async def update(self, dto: SearchUpdateDTO) -> SearchDTO:
        stmt = (update(self.model)
                .where(self.model.id == dto.id)
                .values(**dto.to_orm_values())
                .returning(self.model))
        result = await self._uow.session.execute(stmt)
        await self._uow.session.commit()
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
