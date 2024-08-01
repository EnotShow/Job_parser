import asyncio

from src.api.auth.auth_dto import UserLoginDTO, UserRegisterDTO
from src.api.users.user_dto import UserCreateDTO
from src.client.base import JobParserClient


async def test_auth():
    client = JobParserClient()
    user = UserLoginDTO(email="testuser@mail.com", password="TestPassword")
    await client.auth_as_user(user)

    assert client.session.headers["Authorization"]
    assert await client.verify_token()

    await client.refresh_access_token()
    assert client.session.headers["Authorization"]
    assert await client.verify_token()


async def test_create_user():
    client = JobParserClient()
    user = UserRegisterDTO(
        email="testuser@mail.com",
        password="TestPassword",
        language_code="en",
        refer_id=0,
    )
    r = await client.register(user)
    assert r.status_code == 200
