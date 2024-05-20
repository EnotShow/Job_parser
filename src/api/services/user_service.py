from dependency_injector.wiring import inject

from src.api.dependencies.IUserRepository import IUserRepository
from src.api.dtos.user_dto import UserDTO


class UserService:

    @inject
    def __init__(self, repository=IUserRepository):
        self.repository = repository

    async def get_user(self, dto: UserDTO):
        return await self.repository.get(dto)

    async def get_all_user(self, dto: UserDTO):
        return await self.repository.get_all(dto)

    async def add_user(self, dto: UserDTO):
        return await self.repository.create(dto)

    async def update_user(self, dto: UserDTO):
        return await self.repository.update(dto)

    async def delete_user(self, dto: UserDTO):
        return await self.repository.delete(dto)
