import asyncio

from src.client.base import JobParserClient


async def test_auth():
    client = JobParserClient()
    await client.auth_as_user("enotshow275@gmail.com", "Bunograd")

    assert client.session.headers["Authorization"]
    assert await client.verify_token()

    await client.refresh_access_token()
    assert client.session.headers["Authorization"]
    assert await client.verify_token()
