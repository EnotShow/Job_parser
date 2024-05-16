from dependency_injector.wiring import inject

from src.api.dependencies.ISearch import ISearchRepository


class SearchService:

    @inject
    def __init__(self, repository=ISearchRepository):
        self.repository = repository

    async def get_search(self, ):
        return await self.repository.get()

    async def get_all_search(self, ):
        return await self.repository.get_all()

    async def add_search(self, ):
        return await self.repository.create()

    async def update_search(self, ):
        return await self.repository.update()

    async def delete_search(self, ):
        return await self.repository.delete()
