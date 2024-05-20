from dependency_injector.wiring import inject

from src.api.dependencies.ISearchRepository import ISearchRepository
from src.api.dtos.search_dto import SearchDTO


class SearchService:

    @inject
    def __init__(self, repository=ISearchRepository):
        self.repository = repository

    async def get_search(self, dto: SearchDTO):
        return await self.repository.get(dto)

    async def get_all_search(self, dto: SearchDTO):
        return await self.repository.get_all(dto)

    async def add_search(self, dto: SearchDTO):
        return await self.repository.create(dto)

    async def update_search(self, dto: SearchDTO):
        return await self.repository.update(dto)

    async def delete_search(self, dto: SearchDTO):
        return await self.repository.delete(dto)
