from typing import List

from src.api.searches.search_dto import SearchDTO


class SearchesServiceClient:
    def __init__(self, client):
        self.client = client
        self.base_url = f"{self.client.base_url}/service"

    async def get_searches(self) -> List[SearchDTO]:
        response = await self.client.session.get(f"{self.base_url}/")
        return [SearchDTO(**search) for search in response.json()]

    async def get_search_by_id(self, search_id: int) -> SearchDTO:
        response = await self.client.session.get(f"{self.base_url}/{search_id}")
        return SearchDTO(**response.json())

    async def create_search(self, data: SearchDTO) -> SearchDTO:
        response = await self.client.session.post(f"{self.base_url}/", json=data)
        return SearchDTO(**response.json())

    # async def update_search(self, data: SearchDTO, search_id: int) -> SearchDTO:
    #     response = await self.client.session.put(f"{self.base_url}/{search_id}", json=data)
    #     return SearchDTO(**response.json())

    async def delete_search(self, search_id: int):
        await self.client.session.delete(f"{self.base_url}/{search_id}")


class SearchClient:
    def __init__(self, client):
        self.service = SearchesServiceClient(self)

        self.client = client
        self.base_url = f"{self.client.base_url}/searches"

    async def get_searches(self) -> List[SearchDTO]:
        response = await self.client.session.get(f"{self.base_url}/")
        return [SearchDTO(**search) for search in response.json()]

    async def get_search_by_id(self, search_id: int) -> SearchDTO:
        response = await self.client.session.get(f"{self.base_url}/{search_id}")
        return SearchDTO(**response.json())

    async def create_search(self, data: SearchDTO) -> SearchDTO:
        response = await self.client.session.post(f"{self.base_url}/", json=data)
        return SearchDTO(**response.json())

    async def update_search(self, data: SearchDTO, search_id: int) -> SearchDTO:
        response = await self.client.session.put(f"{self.base_url}/{search_id}", json=data)
        return SearchDTO(**response.json())

    async def delete_search(self, search_id: int):
        await self.client.session.delete(f"{self.base_url}/{search_id}")

