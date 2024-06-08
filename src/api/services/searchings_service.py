from dependency_injector.wiring import inject, Provide

from src.api.containers.repositories_containers.search_repository_container import SearchRepositoryContainer
from src.api.dtos.search_dto import SearchCreateDTO, SearchDTO, SearchFilterDTO
from src.api.repositories.searchings_repository import SearchRepository


class SearchService:

    @inject
    def __init__(self, repository: SearchRepository = Provide[SearchRepositoryContainer.search_repository]):
        self._repository = repository

    async def get_all_searches(self):
        return await self._repository.get()

    async def get_search(self, id: int):
        try:
            return await self._repository.get_single(id)
        except Exception as e:
            return None

    async def create_search(self, dto: SearchCreateDTO):
        try:
            return await self._repository.create(dto)
        except Exception as e:
            return None

    async def update_search(self, dto: SearchDTO, filters: SearchFilterDTO) -> SearchDTO:
        try:
            return await self._repository.update(dto, filters)
        except Exception as e:
            return None

    async def delete_search(self, id: int):
        try:
            return await self._repository.delete(id)
        except Exception as e:
            return None
