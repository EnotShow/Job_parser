import asyncio

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:

    def __init__(self, db_session: AsyncSession):
        self._session = db_session
