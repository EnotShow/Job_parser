from dependency_injector import containers, providers

from core.db.db_helper import db_helper


class AsyncSessionContainer(containers.DeclarativeContainer):
    db_session = providers.Callable(db_helper.get_session)
