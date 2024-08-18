import httpx

from core.config.proj_settings import settings, development_settings
from src.api.auth.auth_dto import UserRegisterDTO, UserLoginDTO
from src.client.ApplicationClient import ApplicationClient
from src.client.BaseClient import BaseClient
from src.client.NotificationClient import NotificationsClient
from src.client.SearchClient import SearchClient
from src.client.TelegramClient import TelegramClient
from src.client.UserClient import UserClient


class JobParserClient(BaseClient):
    def __init__(self, base_url: str = settings.base_url):
        self.base_url = base_url
        self.session = httpx.AsyncClient()
        self.refresh_token = None

        self.users = UserClient(self)
        self.applications = ApplicationClient(self)
        self.searches = SearchClient(self)
        self.notifications = NotificationsClient(self)
        self.telegram = TelegramClient(self)

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

    async def auth_as_service(self, api_token: str):
        self.session.headers["X-Api-Key"] = api_token
        self.refresh_token = None

    async def auth_by_hash(self, _hash: str):
        tokens = await self.session.get(
            f"{self.base_url}/auth/login/{_hash}",
        )
        if tokens.status_code != 200:
            raise Exception

        self.session.headers["Authorization"] = f"Bearer {tokens.json()['access_token']}"
        self.refresh_token = tokens.json()["refresh_token"]

        return tokens
