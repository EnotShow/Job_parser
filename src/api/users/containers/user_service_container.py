from dependency_injector import containers, providers

from src.api.users.containers.user_repository_container import UserRepositoryContainer
from src.api.users.user_service import UserService


class UserServiceContainer(containers.DeclarativeContainer):
    repository_container = providers.Container(UserRepositoryContainer)

    user_service = providers.Factory(
        UserService,
        repository=repository_container.user_repository,
    )