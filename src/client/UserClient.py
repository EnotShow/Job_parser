from typing import Union
from httpx import Response  # Importing Response from httpx

from src.api.users.user_dto import UserUpdateDTO, UserDTO, UserSettingsDTO
from src.client.BaseClient import BaseClient


class UserServiceClient(BaseClient):
    def __init__(self, client):
        self.client = client
        self.session = client.session
        self.base_url = f"{self.client.base_url}/service"

    async def get_user(self, user_id: int, *, return_response: bool = False) -> Union[UserDTO, Response]:
        response = await self.session.get(f"{self.base_url}/{user_id}")
        if return_response:
            return response
        return UserDTO(**response.json())

    async def update_user(self, data: UserUpdateDTO, user_id: int, *, return_response: bool = False) -> Union[UserDTO, Response]:
        response = await self.session.put(f"{self.base_url}/{user_id}", json=data.dict())
        if return_response:
            return response
        return UserDTO(**response.json())

    async def get_user_settings(self, user_id: int, *, return_response: bool = False) -> Union[UserSettingsDTO, Response]:
        response = await self.session.get(f"{self.base_url}/settings/{user_id}")
        if return_response:
            return response
        return UserSettingsDTO(**response.json())

    async def delete_user(self, user_id: int, *, return_response: bool = False) -> Union[None, Response]:
        response = await self.session.delete(f"{self.base_url}/{user_id}")
        if return_response:
            return response


class UserClient:
    def __init__(self, client):
        self.client = client
        self.session = client.session
        self.base_url = f"{self.client.base_url}/users"

        self.service = UserServiceClient(self)

    async def get_me(self, *, return_response: bool = False) -> Union[UserDTO, Response]:
        response = await self.session.get(f"{self.base_url}/me")
        if return_response:
            return response
        return UserDTO(**response.json())

    async def update_me(self, data: UserUpdateDTO, *, return_response: bool = False) -> Union[UserDTO, Response]:
        response = await self.session.put(f"{self.base_url}/me", json=data.dict())
        if return_response:
            return response
        return UserDTO(**response.json())

    async def get_settings(self, *, return_response: bool = False) -> Union[UserSettingsDTO, Response]:
        response = await self.session.get(f"{self.base_url}/me/settings")
        if return_response:
            return response
        return UserSettingsDTO(**response.json())

    async def get_user_settings_by_id(self, user_id: int, *, return_response: bool = False) -> Union[UserSettingsDTO, Response]:
        response = await self.session.get(f"{self.base_url}/settings/{user_id}")
        if return_response:
            return response
        return UserSettingsDTO(**response.json())
