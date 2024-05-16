from typing import Annotated

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

from core.db.db_helper import db_helper
from src.repositories.application_repository import ApplicationRepository


class IApplicationContainer(containers.DeclarativeContainer):
    application_repository = providers.Factory(
        ApplicationRepository, db_session=providers.Resource(db_helper.get_db_session)
    )


IApplicationRepository = Annotated[ApplicationRepository, Provide[IApplicationContainer.application_repository]]
