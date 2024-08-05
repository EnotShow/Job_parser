from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession

from core.config.db import settings_db
from core.db.uow import UnitOfWork


class DatabaseHelper:
    """
    Class for working with database
    """

    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scope_session(self):
        return async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )

    async def get_unit_of_work(self) -> UnitOfWork:
        return UnitOfWork(self.session_factory)

    @asynccontextmanager
    async def get_db_session(self):
        from sqlalchemy import exc

        session: AsyncSession = self.session_factory()
        try:
            yield session
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def get_session(self) -> AsyncSession:
        return self.session_factory()


db_helper = DatabaseHelper(settings_db.database_url, settings_db.DB_ECHO_LOG)
