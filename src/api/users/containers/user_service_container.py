from dependency_injector import containers, providers

from core.shared.async_session_container import UnitOfWorkContainer
from src.api.users.user_service import UserService


class UserServiceContainer(containers.DeclarativeContainer):
    uow = providers.Container(UnitOfWorkContainer)

    user_service = providers.Factory(
        UserService,
        uow=uow.uow
    )
