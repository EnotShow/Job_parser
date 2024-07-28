import asyncio

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:

    def __init__(self, db_session: AsyncSession):
        self._session = db_session

    def __del__(self):
        if self._session is not None:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
            loop.create_task(self._session.close())
