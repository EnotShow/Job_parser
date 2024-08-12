import faker as _faker
import pytest

from src.api.auth.auth_dto import UserRegisterDTO, UserLoginDTO
from src.client.client import JobParserClient
from tests.fixtures.helpers import decode_token


@pytest.fixture
def client():
    client = JobParserClient()
    return client


@pytest.fixture()
def faker():
    faker = _faker.Faker()
    return faker


@pytest.fixture()
async def service_client():
    client = JobParserClient()
    await client.auth_as_service()
    return client


@pytest.fixture()
async def base_user(client: JobParserClient, faker: _faker.Faker):
    user = UserRegisterDTO(
        email=faker.email(),
        password=faker.password(),
        language_code=faker.language_code(),
        refer_id=0,
    )
    tokens = await client.register(user)
    data = await decode_token(tokens.json()["refresh_token"])
    yield data.user
    user = data.user
    await client.auth_as_service()
    await client.users.service.delete_user(user.id)


@pytest.fixture()
async def created_user(client: JobParserClient, faker: _faker.Faker):
    user = UserRegisterDTO(
        email=faker.email(),
        password=faker.password(),
        language_code=faker.language_code(),
        refer_id=0,
    )
    tokens = await client.register(user)
    data = await decode_token(tokens.json()["refresh_token"])
    yield user
    user = data.user
    await client.auth_as_service()
    await client.users.service.delete_user(user.id)


@pytest.fixture()
async def user_client(client: JobParserClient, faker: _faker.Faker):
    user = UserRegisterDTO(
        email=faker.email(),
        password=faker.password(),
        language_code=faker.language_code(),
        refer_id=0,
    )
    tokens = await client.register(user)
    await client.auth_as_user(UserLoginDTO(email=user.email, password=user.password))
    yield client
    data = await decode_token(tokens.json()["refresh_token"])
    user = data.user
    await client.auth_as_service()
    await client.users.service.delete_user(user.id)
