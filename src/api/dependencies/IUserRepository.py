from typing import Annotated

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

from core.db.db_helper import db_helper
from src.api.repositories.user_repository import UserRepository


class IUserContainer(containers.DeclarativeContainer):
    user_repository = providers.Factory(
        UserRepository, db_session=providers.Resource(db_helper.get_db_session)
    )


IUserRepository = Annotated[UserRepository, Provide[IUserContainer.user_repository]]
