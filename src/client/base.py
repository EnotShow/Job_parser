import httpx

from core.config.proj_settings import settings


class JobParserClient:
    # user_client = UserClient()
    # application_client = ApplicationClient()
    # search_client = SearchClient()

    def __init__(self, base_url: str = settings.base_url):
        self.base_url = base_url
        self.session = httpx.AsyncClient()
        self.refresh_token = None

    async def auth_as_user(self, email: str, password: str):
        tokens = await self.session.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password},
        )
        if tokens.status_code != 200:
            raise Exception

        self.session.headers["Authorization"] = f"Bearer {tokens.json()['access_token']}"
        self.refresh_token = tokens.json()["refresh_token"]

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

    async def verify_token(self):
        tokens = await self.session.get(
            f"{self.base_url}/auth/verify_token",
        )
        if tokens.status_code != 200:
            raise Exception

        return True if tokens.status_code == 200 else False
