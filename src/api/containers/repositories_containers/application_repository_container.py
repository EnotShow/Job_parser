from dependency_injector import containers, providers

from core.shared.async_session_container import AsyncSessionContainer
from src.api.repositories.application_repository import ApplicationRepository


class ApplicationRepositoryContainer(containers.DeclarativeContainer):
    db_session_container = providers.Container(AsyncSessionContainer)

    application_repository = providers.Factory(
        ApplicationRepository,
        db_session=db_session_container.db_session,
    )
