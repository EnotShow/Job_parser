from typing import List, Union
from httpx import Response

from src.api.applications.application_dto import (
    ApplicationDTO,
    ApplicationUpdateDTO,
    ApplicationCreateDTO,
    ApplicationFilterDTO
)
from src.client.BaseClient import BaseClient


class ApplicationServiceClient(BaseClient):
    def __init__(self, client):
        self.client = client
        self.session = client.session
        self.base_url = f"{self.client.base_url}/service"

    async def get_application(self, application_id: int, *, return_response: bool = False) -> Union[ApplicationDTO, Response]:
        response = await self.session.get(f"{self.base_url}/{application_id}")
        if return_response:
            return response
        return ApplicationDTO(**response.json())

    async def update_application(self, data: ApplicationUpdateDTO, application_id: int, *, return_response: bool = False) -> Union[ApplicationDTO, Response]:
        response = await self.session.put(f"{self.base_url}/{application_id}", json=data.dict())
        if return_response:
            return response
        return ApplicationDTO(**response.json())

    async def create_application(self, data: ApplicationCreateDTO, *, return_response: bool = False) -> Union[ApplicationDTO, Response]:
        response = await self.session.post(f"{self.base_url}/", json=data.dict())
        if return_response:
            return response
        return ApplicationDTO(**response.json())

    async def get_all_applications(self, *, limit: int = None, page: int = None, return_response: bool = False) -> Union[List[ApplicationDTO], Response]:
        url = self._add_pagination(f"{self.base_url}/", limit, page)
        response = await self.session.get(url)
        if return_response:
            return response
        return [ApplicationDTO(**application) for application in response.json()['items']]

    async def get_applications_if_exists(
        self,
        data: Union[ApplicationFilterDTO, List[ApplicationFilterDTO]],
        *,
        limit: int = None,
        page: int = None,
        return_response: bool = False
    ) -> Union[List[ApplicationDTO], Response]:
        url = self._add_pagination(f"{self.base_url}/find_multiple", limit, page) if limit or page else f"{self.base_url}/find_multiple"
        response = await self.session.post(url, json=[item.dict() for item in data] if isinstance(data, list) else data.dict())
        if return_response:
            return response
        return [ApplicationDTO(**application) for application in response.json()['items']]

    async def create_multiple_applications(self, data: List[ApplicationCreateDTO], *, return_response: bool = False) -> Union[List[ApplicationDTO], Response]:
        response = await self.session.post(f"{self.base_url}/create_multiple", json=[item.dict() for item in data])
        if return_response:
            return response
        return [ApplicationDTO(**application) for application in response.json()]


class ApplicationClient(BaseClient):
    def __init__(self, client):
        self.client = client
        self.session = client.session
        self.base_url = f"{self.client.base_url}/applications"

        self.service = ApplicationServiceClient(self)

    async def get_all_applications(self, *, limit: int = None, page: int = None, return_response: bool = False) -> Union[List[ApplicationDTO], Response]:
        url = self._add_pagination(f"{self.base_url}/", limit, page)
        response = await self.session.get(url)
        if return_response:
            return response
        return [ApplicationDTO(**application) for application in response.json()['items']]

    async def get_application(self, application_id: int, *, return_response: bool = False) -> Union[ApplicationDTO, Response]:
        response = await self.session.get(f"{self.base_url}/{application_id}")
        if return_response:
            return response
        return ApplicationDTO(**response.json())

    async def get_applied_applications(self, user_id: int, *, limit: int = None, page: int = None, return_response: bool = False) -> Union[List[ApplicationDTO], Response]:
        url = self._add_pagination(f"{self.base_url}/applied", limit, page)
        response = await self.session.get(url)
        if return_response:
            return response
        return [ApplicationDTO(**application) for application in response.json()['items']]

    async def update_application(self, data: ApplicationDTO, application_id: int, *, return_response: bool = False) -> Union[ApplicationDTO, Response]:
        response = await self.session.put(f"{self.base_url}/{application_id}", json=data.dict())
        if return_response:
            return response
        return ApplicationDTO(**response.json())
