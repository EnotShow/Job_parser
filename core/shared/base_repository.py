import asyncio

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:

    def __init__(self, db_session: AsyncSession):
        self._session = db_session

    def __del__(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self._session.close())