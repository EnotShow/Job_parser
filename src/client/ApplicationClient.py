from typing import List, Union

from src.api.applications.application_dto import ApplicationDTO, ApplicationUpdateDTO, ApplicationCreateDTO, \
    ApplicationFilterDTO


class ApplicationServiceClient:
    def __init__(self, client):
        self.client = client
        self.base_url = f"{self.client.base_url}/service"

    async def get_application(self, application_id: int) -> ApplicationDTO:
        response = await self.client.session.get(f"{self.base_url}/{application_id}")
        return ApplicationDTO(**response.json())

    async def update_application(self, data: ApplicationUpdateDTO, application_id: int) -> ApplicationDTO:
        response = await self.client.session.put(f"{self.base_url}/{application_id}", json=data)
        return ApplicationDTO(**response.json())

    async def create_application(self, data: ApplicationCreateDTO) -> ApplicationDTO:
        response = await self.client.session.post(f"{self.base_url}/", json=data)
        return ApplicationDTO(**response.json())

    async def get_all_applications(self) -> List[ApplicationDTO]:
        response = await self.client.session.get(f"{self.base_url}/")
        return [ApplicationDTO(**application) for application in response.json()]

    async def get_applications_if_exists(self, data: Union[ApplicationFilterDTO, List[ApplicationFilterDTO]]) -> List[ApplicationDTO]:
        response = await self.client.session.post(f"{self.base_url}/find_multiple", json=data)
        return [ApplicationDTO(**application) for application in response.json()]

    async def create_multiple_applications(self, data: List[ApplicationCreateDTO]) -> List[ApplicationDTO]:
        response = await self.client.session.post(f"{self.base_url}/create_multiple", json=data)
        return [ApplicationDTO(**application) for application in response.json()]


class ApplicationClient:
    def __init__(self, client):
        self.service = ApplicationServiceClient(self)

        self.client = client
        self.base_url = f"{self.client.base_url}/applications"

    async def get_all_applications(self) -> List[ApplicationDTO]:
        response = await self.client.session.get(f"{self.base_url}/")
        return [ApplicationDTO(**application) for application in response.json()]

    async def get_application(self, application_id: int) -> ApplicationDTO:
        response = await self.client.session.get(f"{self.base_url}/{application_id}")
        return ApplicationDTO(**response.json())

    async def get_applied_applications(self, user_id: int) -> List[ApplicationDTO]:
        response = await self.client.session.get(f"{self.base_url}/applied")
        return [ApplicationDTO(**application) for application in response.json()]

    async def update_application(self, data: ApplicationDTO, application_id: int) -> ApplicationDTO:
        response = await self.client.session.put(f"{self.base_url}/{application_id}", json=data)
        return ApplicationDTO(**response.json())
