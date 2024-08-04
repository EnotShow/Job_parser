import asyncio

from src.api.auth.auth_dto import UserLoginDTO
from src.client.base import JobParserClient


async def main():
    client = JobParserClient()
    print(client.base_url)
    await client.auth_as_user(data=UserLoginDTO(email='enotshow275@gmail.com', password='Bunograd7$'))
    print(await client.searches.get_searches())


if __name__ == '__main__':
    asyncio.run(main())
