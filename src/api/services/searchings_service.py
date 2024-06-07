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
        return await self._repository.get_single(id)

    async def create_search(self, dto: SearchCreateDTO):
        return await self._repository.create(dto)

    async def update_search(self, dto: SearchDTO, filters: SearchFilterDTO) -> SearchDTO:
        return await self._repository.update(dto, filters)

    async def delete_search(self, id: int):
        return await self._repository.delete(id)
