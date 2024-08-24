from typing import List, Union
from httpx import Response
from src.api.searches.search_dto import SearchDTO
from src.client.BaseClient import BaseClient


class SearchesServiceClient(BaseClient):
    def __init__(self, client):
        self.client = client
        self.session = client.session
        self.base_url = f"{self.client.base_url}/service"

    async def get_searches(self, *, limit: int = None, page: int = None, return_response: bool = False) -> Union[List[SearchDTO], Response]:
        url = self._add_pagination(f"{self.base_url}/", limit, page)
        response = await self.session.get(url)
        if return_response:
            return response
        return [SearchDTO(**search) for search in response.json()['items']]

    async def get_search_by_id(self, search_id: int, *, return_response: bool = False) -> Union[SearchDTO, Response]:
        response = await self.session.get(f"{self.base_url}/{search_id}")
        if return_response:
            return response
        return SearchDTO(**response.json())

    async def create_search(self, data: SearchDTO, *, return_response: bool = False) -> Union[SearchDTO, Response]:
        response = await self.session.post(f"{self.base_url}/", json=data.dict())
        if return_response:
            return response
        return SearchDTO(**response.json())

    async def create_searches(self, data: List[SearchDTO], *, return_response: bool = False) -> Union[List[SearchDTO], Response]:
        response = await self.session.post(f"{self.base_url}/create_multiple", json=[item.dict() for item in data])
        if return_response:
            return response
        return [SearchDTO(**search) for search in response.json()]

    async def update_search(self, data: SearchDTO, search_id: int, *, return_response: bool = False) -> Union[SearchDTO, Response]:
        response = await self.session.put(f"{self.base_url}/{search_id}", json=data.dict())
        if return_response:
            return response
        return SearchDTO(**response.json())

    async def delete_search(self, search_id: int, *, return_response: bool = False) -> Union[None, Response]:
        response = await self.session.delete(f"{self.base_url}/{search_id}")
        if return_response:
            return response


class SearchClient(BaseClient):
    def __init__(self, client):
        self.client = client
        self.session = client.session
        self.base_url = f"{self.client.base_url}/searches"

        self.service = SearchesServiceClient(self)

    async def get_searches(self, *, limit: int = None, page: int = None, return_response: bool = False) -> Union[List[SearchDTO], Response]:
        url = self._add_pagination(f"{self.base_url}/", limit, page)
        response = await self.session.get(url)
        if return_response:
            return response
        return [SearchDTO(**search) for search in response.json()['items']]

    async def get_search_by_id(self, search_id: int, *, return_response: bool = False) -> Union[SearchDTO, Response]:
        response = await self.session.get(f"{self.base_url}/{search_id}")
        if return_response:
            return response
        return SearchDTO(**response.json())

    async def create_search(self, data: SearchDTO, *, return_response: bool = False) -> Union[SearchDTO, Response]:
        response = await self.session.post(f"{self.base_url}/", json=data.dict())
        if return_response:
            return response
        return SearchDTO(**response.json())

    async def create_searches(self, data: List[SearchDTO], *, return_response: bool = False) -> Union[List[SearchDTO], Response]:
        response = await self.session.post(f"{self.base_url}/create_multiple", json=[item.dict() for item in data])
        if return_response:
            return response
        return [SearchDTO(**search) for search in response.json()]

    async def update_search(self, data: SearchDTO, search_id: int, *, return_response: bool = False) -> Union[SearchDTO, Response]:
        response = await self.session.put(f"{self.base_url}/{search_id}", json=data.dict())
        if return_response:
            return response
        return SearchDTO(**response.json())

    async def delete_search(self, search_id: int, *, return_response: bool = False) -> Union[None, Response]:
        response = await self.session.delete(f"{self.base_url}/{search_id}")
        if return_response:
            return response
