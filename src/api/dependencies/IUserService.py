from typing import Annotated

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

from src.api.dependencies.IUserRepository import IUserRepository
from src.api.services.user_service import UserService


class IUserContainer(containers.DeclarativeContainer):

    user_service = providers.Factory(
        UserService, user_repository=IUserRepository
    )


IUserService = Annotated[UserService, Provide[IUserContainer.user_service]]
