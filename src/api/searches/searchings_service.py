from dependency_injector.wiring import inject, Provide

from core.shared.base_service import BaseService
from core.shared.errors import NoRowsFoundError
from src.api.searches.containers.search_repository_container import SearchRepositoryContainer
from src.api.users.containers.user_repository_container import UserRepositoryContainer
from src.api.middleware.dtos.pagination_dto import PaginationDTO
from src.api.searches.search_dto import SearchCreateDTO, SearchDTO, SearchFilterDTO, SearchUpdateDTO
from src.api.users.user_dto import UserFilterDTO
from src.api.searches.searchings_repository import SearchRepository
from src.api.users.user_repository import UserRepository


class SearchService(BaseService):

    @inject
    def __init__(self, repository: SearchRepository = Provide[SearchRepositoryContainer.search_repository]):
        self._repository = repository

    async def get_all_searches(self, limit: int = 10, page: int = 1) -> PaginationDTO[SearchDTO]:
        response_objects = await self._repository.get(limit, page)
        return self._paginate(response_objects, page, len(response_objects))

    async def get_search(self, id: int) -> SearchDTO:
        try:
            return await self._repository.get_single(id)
        except Exception as e:
            raise NoRowsFoundError

    async def get_user_searches(self, user_id: int, limit: int = 10, page: int = 1) -> PaginationDTO[SearchDTO]:
        try:
            filter = SearchFilterDTO(owner_id=user_id)
            response_objects = await self._repository.get_filtered(filter, limit=limit, page=page)
            total = await self._repository.get_count(filter)
            return self._paginate(response_objects, page, len(response_objects), total)
        except Exception as e:
            raise NoRowsFoundError

    async def get_user_search(self, user_id: int, search_id: int) -> SearchDTO:
        try:
            filter = SearchFilterDTO(owner_id=user_id, id=search_id)
            response = await self._repository.get_filtered(filter, limit=1, page=1)
            print(response)
            return response[0]
        except Exception as e:
            raise NoRowsFoundError(f"Search {search_id} not found")

    @inject
    async def get_telegram_user_searches(
            self,
            telegram_id: int,
            limit: int = 10,
            page: int = 1,
            user_repository: UserRepository = Provide[UserRepositoryContainer.user_repository]
    ) -> PaginationDTO[SearchDTO]:
        try:
            find_user_filter = UserFilterDTO(telegram_id=telegram_id)
            user = await user_repository.get_filtered(find_user_filter, limit=1, page=1)
            response_objects = await self._repository.get_filtered(
                SearchFilterDTO(owner_id=user.id), limit=limit, page=page)
            return self._paginate(response_objects, page, len(response_objects))
        except Exception as e:
            raise NoRowsFoundError

    async def create_search(self, dto: SearchCreateDTO) -> SearchDTO:
        try:
            return await self._repository.create(dto)
        except Exception as e:
            raise e

    async def create_user_search(
            self, dto: SearchCreateDTO,
            user_id: int,
            user_repository: UserRepository = Provide[UserRepositoryContainer.user_repository]
    ) -> SearchDTO:
        try:
            if dto.owner_id == user_id:
                user = await user_repository.get_user_settings(user_id)
                search_dto = SearchFilterDTO(owner_id=user.id)
                searches_count = await self._repository.get_count(search_dto)
                if searches_count >= user.links_limit:
                    raise Exception("User links limit reached")
                search_obj = SearchCreateDTO(**dto.model_dump())
                return await self._repository.create(search_obj)
            else:
                raise NoRowsFoundError("User not found")
        except Exception as e:
            raise e

    @inject
    async def crete_search_from_telegram(
            self,
            data: dict,
            telegram_id: int,
            user_repository: UserRepository = Provide[UserRepositoryContainer.user_repository]
    ) -> SearchDTO:
        try:
            user_obj = UserFilterDTO(telegram_id=telegram_id)
            response = await user_repository.get_filtered(user_obj, limit=1, page=1)
            search_obj = SearchCreateDTO(owner_id=response[0].id, **data)
            return await self._repository.create(search_obj)
        except Exception as e:
            raise e

    async def update_search(self, dto: SearchUpdateDTO) -> SearchDTO:
        try:
            return await self._repository.update(dto)
        except Exception as e:
            raise e

    async def update_user_search(self, dto: SearchUpdateDTO, user_id: int) -> SearchDTO:
        try:
            search_dto = SearchFilterDTO(id=dto.id, owner_id=user_id)
            response = await self._repository.get_filtered(search_dto, limit=1, page=1)
            if response:
                return await self._repository.update(dto)
            else:
                raise NoRowsFoundError("Search not found")
        except Exception as e:
            raise NoRowsFoundError("Search not found")

    async def delete_search(self, id: int) -> None:
        try:
            return await self._repository.delete(id)
        except Exception as e:
            raise e

    async def delete_user_search(self, search_id: int, user_id: int,) -> None:
        try:
            search_dto = SearchFilterDTO(id=search_id, owner_id=user_id)
            response = await self._repository.get_filtered(search_dto, limit=1, page=1)
            if response[0] and search_dto.owner_id == user_id:
                return await self._repository.delete(search_id)
            else:
                raise NoRowsFoundError("Search not found")
        except Exception as e:
            raise e
