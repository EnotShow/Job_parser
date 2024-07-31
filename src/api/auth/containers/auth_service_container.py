from dependency_injector import containers, providers

from src.api.users.containers.user_service_container import UserServiceContainer
from src.api.auth.services.auth_service import AuthService


class AuthServiceContainer(containers.DeclarativeContainer):
    service_container = providers.Container(UserServiceContainer)

    auth_service = providers.Factory(
        AuthService,
        user_service=service_container.user_service,
    )
