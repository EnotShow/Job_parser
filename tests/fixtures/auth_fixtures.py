import pytest
import faker as _faker

from src.api.auth.auth_dto import UserRegisterDTO
from src.client.base import JobParserClient


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
    await client.register(user)
    return user
