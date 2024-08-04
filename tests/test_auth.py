import pytest

from src.api.auth.auth_dto import UserLoginDTO, UserRegisterDTO


@pytest.mark.auth
async def test_auth(client, base_user):
    base_user = await base_user
    user = UserLoginDTO(email=base_user.email(), password=base_user.password())
    await client.auth_as_user(user)

    assert client.session.headers["Authorization"]
    assert await client.verify_token()

    await client.refresh_access_token()
    assert client.session.headers["Authorization"]
    assert await client.verify_token()


@pytest.mark.auth
async def test_create_user(client, faker):
    user = UserRegisterDTO(
        email=faker.email(),
        password=faker.password(),
        language_code=faker.language_code(),
        refer_id=0,
    )
    r = await client.register(user)
    assert r.status_code == 200
