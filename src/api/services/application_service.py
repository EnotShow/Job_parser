from dependency_injector.wiring import inject

from src.api.dependencies.IApplication import IApplicationRepository


class ApplicationService:

    @inject
    def __init__(self, repository=IApplicationRepository):
        self.repository = repository

    async def get_application(self, ):
        return await self.repository.get()

    async def get_all_application(self, ):
        return await self.repository.get_all()

    async def add_application(self, ):
        return await self.repository.create()

    async def update_application(self, ):
        return await self.repository.update()

    async def delete_application(self, ):
        return await self.repository.delete()
