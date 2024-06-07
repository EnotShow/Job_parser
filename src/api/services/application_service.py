from dependency_injector.wiring import inject, Provide

from src.api.containers.repositories_containers.application_repository_container import ApplicationRepositoryContainer
from src.api.dtos.application_dto import ApplicationCreateDTO, ApplicationDTO, ApplicationFilterDTO
from src.api.repositories.application_repository import ApplicationRepository


class ApplicationService:

    @inject
    def __init__(self, repository: ApplicationRepository = Provide[ApplicationRepositoryContainer.application_repository]):
        self._repository = repository

    async def get_all_applications(self):
        return await self._repository.get()

    async def get_application(self, id: int):
        return await self._repository.get_single(id)

    async def create_application(self, dto: ApplicationCreateDTO):
        return await self._repository.create(dto)

    async def update_application(self, dto: ApplicationDTO, filters: ApplicationFilterDTO):
        return await self._repository.update(dto, filters)

    async def delete_application(self, id: int):
        return await self._repository.delete(id)