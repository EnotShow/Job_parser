import httpx

from core.config.proj_settings import settings
from src.api.auth.auth_dto import UserRegisterDTO, UserLoginDTO
from src.client.UserClient import UserClient


class JobParserClient:
    def __init__(self, base_url: str = settings.base_url):
        users = UserClient(self)

        self.base_url = base_url
        self.session = httpx.AsyncClient()
        self.refresh_token = None

    async def auth_as_user(self, data: UserLoginDTO):
        tokens = await self.session.post(
            f"{self.base_url}/auth/login",
            json=data.model_dump(),
        )
        if tokens.status_code != 200:
            raise Exception

        self.session.headers["Authorization"] = f"Bearer {tokens.json()['access_token']}"
        self.refresh_token = tokens.json()["refresh_token"]

        return tokens

    async def refresh_access_token(self):
        tokens = await self.session.post(
            f"{self.base_url}/auth/refresh",
            json={"refresh_token": self.refresh_token},
        )
        if tokens.status_code != 200:
            raise Exception

        self.session.headers["Authorization"] = f"Bearer {tokens.json()['access_token']}"
        print(tokens.json())
        self.refresh_token = tokens.json()["access_token"]

        return tokens

    async def verify_token(self):
        tokens = await self.session.get(
            f"{self.base_url}/auth/verify_token",
        )
        if tokens.status_code != 200:
            raise Exception

        return True if tokens.status_code == 200 else False

    async def register(self, data: UserRegisterDTO):
        tokens = await self.session.post(
            f"{self.base_url}/auth/register",
            json=data.model_dump(),
        )
        if tokens.status_code != 200:
            raise Exception

        return tokens

    async def auth_as_service(self):
        self.session.headers["X-Api-Key"] = settings.service_api_key
        self.refresh_token = None
