from dependency_injector import containers, providers

from core.shared.async_session_container import AsyncSessionContainer
from src.api.users.user_repository import UserRepository


class UserRepositoryContainer(containers.DeclarativeContainer):
    db_session_container = providers.Container(AsyncSessionContainer)

    user_repository = providers.Factory(
        UserRepository,
        db_session=db_session_container.db_session,
    )
