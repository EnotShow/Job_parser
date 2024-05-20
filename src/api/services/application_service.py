from dependency_injector.wiring import inject

from src.api.dependencies.IApplicationRepository import IApplicationRepository
from src.api.dtos.application_dto import ApplicationDTO


class ApplicationService:

    @inject
    def __init__(self, repository=IApplicationRepository):
        self.repository = repository

    async def get_application(self, dto: ApplicationDTO):
        return await self.repository.get(dto)

    async def get_all_application(self, dto: ApplicationDTO):
        return await self.repository.get_all(dto)

    async def add_application(self, dto: ApplicationDTO):
        return await self.repository.create(dto)

    async def update_application(self, dto: ApplicationDTO):
        return await self.repository.update(dto)

    async def delete_application(self, dto):
        return await self.repository.delete()
