from dependency_injector.wiring import inject

from src.api.dependencies.IUser import IUserRepository


class UserService:

    @inject
    def __init__(self, repository=IUserRepository):
        self.repository = repository

    async def get_user(self, ):
        return await self.repository.get()

    async def get_all_user(self, ):
        return await self.repository.get_all()

    async def add_user(self, ):
        return await self.repository.create()

    async def update_user(self, ):
        return await self.repository.update()

    async def delete_user(self, ):
        return await self.repository.delete()
