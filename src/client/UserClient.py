from src.api.users.user_dto import UserUpdateDTO, UserDTO, UserSettingsDTO, UserSelfUpdateDTO
from src.client.BaseClient import BaseClient


class UserServiceClient(BaseClient):
    def __init__(self, client):
        self.client = client
        self.base_url = f"{self.client.base_url}/service"

    async def get_user(self, user_id: int) -> UserDTO:
        response = await self.client.session.get(f"{self.base_url}/{user_id}")
        return UserDTO(**response.json())

    async def update_user(self, data: UserUpdateDTO, user_id: int) -> UserDTO:
        response = await self.client.session.put(f"{self.base_url}/{user_id}", json=data)
        return UserDTO(**response.json())

    async def get_user_settings(self, user_id: int) -> UserSettingsDTO:
        response = await self.client.session.get(f"{self.base_url}/settings/{user_id}")
        return UserSettingsDTO(**response.json())

    async def delete_user(self, user_id: int):
        await self.client.session.delete(f"{self.base_url}/{user_id}")


class UserClient:
    def __init__(self, client):
        self.client = client
        self.base_url = f"{self.client.base_url}/users"

        self.service = UserServiceClient(self)

    async def get_me(self) -> UserDTO:
        response = await self.client.session.get(f"{self.base_url}/me")
        return UserDTO(**response.json())

    async def update_me(self, data: UserSelfUpdateDTO) -> UserDTO:
        response = await self.client.session.put(f"{self.base_url}/me", json=data)
        return UserDTO(**response.json())

    async def get_settings(self) -> UserSettingsDTO:
        response = await self.client.session.get(f"{self.base_url}/me/settings")
        return UserSettingsDTO(**response.json())

    async def get_user_settings_by_id(self, user_id: int) -> dict:
        return await self.client.session.get(f"{self.base_url}/settings/{user_id}")