from typing import List

from dependency_injector.wiring import inject, Provide

from core.shared.base_service import BaseService
from core.shared.errors import NoRowsFoundError
from src.api.containers.repositories_containers.search_repository_container import SearchRepositoryContainer
from src.api.containers.repositories_containers.user_repository_container import UserRepositoryContainer
from src.api.dtos.search_dto import SearchCreateDTO, SearchDTO, SearchFilterDTO, SearchUpdateDTO
from src.api.dtos.user_dto import UserFilterDTO
from src.api.repositories.searchings_repository import SearchRepository
from src.api.repositories.user_repository import UserRepository


class SearchService(BaseService):

    @inject
    def __init__(self, repository: SearchRepository = Provide[SearchRepositoryContainer.search_repository]):
        self._repository = repository

    async def get_all_searches(self, limit: int = 10, page: int = 1) -> List[SearchDTO]:
        return await self._repository.get(limit, page)

    async def get_search(self, id: int):
        try:
            return await self._repository.get_single(id)
        except Exception as e:
            raise NoRowsFoundError

    async def get_user_searches(self, user_id: int):
        try:
            filter = SearchFilterDTO(owner_id=user_id)
            return await self._repository.get_filtered(filter)
        except Exception as e:
            raise NoRowsFoundError

    @inject
    async def get_telegram_user_searches(
            self,
            telegram_id: int,
            user_repository: UserRepository = Provide[UserRepositoryContainer.user_repository]
    ):
        try:
            find_user_filter = UserFilterDTO(telegram_id=telegram_id)
            user = self._unpack_items(await user_repository.get_filtered(find_user_filter, limit=1, page=1))
            return await self.get_user_searches(user["id"])
        except Exception as e:
            raise NoRowsFoundError

    async def create_search(self, dto: SearchCreateDTO):
        try:
            return await self._repository.create(dto)
        except Exception as e:
            raise e

    @inject
    async def crete_search_from_telegram(
            self,
            data: dict,
            telegram_id: int,
            user_repository: UserRepository = Provide[UserRepositoryContainer.user_repository]
    ):
        try:
            user_obj = UserFilterDTO(telegram_id=telegram_id)
            user = await user_repository.get_filtered(user_obj, get_single=True)
            search_obj = SearchCreateDTO(owner_id=user.id, **data)
            return await self._repository.create(search_obj)
        except Exception as e:
            raise e

    async def update_search(self, dto: SearchUpdateDTO) -> [SearchDTO, None]:
        try:
            return await self._repository.update(dto)
        except Exception as e:
            raise e

    async def delete_search(self, id: int):
        try:
            return await self._repository.delete(id)
        except Exception as e:
            raise e
