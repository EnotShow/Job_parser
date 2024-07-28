from dependency_injector import containers, providers

from src.api.containers.services_containers.user_service_container import UserServiceContainer
from src.api.services.auth_service import AuthService


class AuthServiceContainer(containers.DeclarativeContainer):
    service_container = providers.Container(UserServiceContainer)

    auth_service = providers.Factory(
        AuthService,
        user_service=service_container.user_service,
    )
