from dependency_injector import containers, providers

from core.db.db_helper import db_helper
from core.shared.async_session_container import AsyncSessionContainer
from src.api.repositories.user_repository import UserRepository


class UserRepositoryContainer(containers.DeclarativeContainer):
    db_session_container = providers.Container(AsyncSessionContainer)

    user_repository = providers.Factory(
        UserRepository,
        db_session=db_session_container.db_session,
    )
