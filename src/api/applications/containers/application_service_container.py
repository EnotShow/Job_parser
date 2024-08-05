from dependency_injector import containers, providers

from core.shared.async_session_container import UnitOfWorkContainer
from src.api.applications.application_service import ApplicationService


class ApplicationServiceContainer(containers.DeclarativeContainer):
    repository_container = providers.Container(UnitOfWorkContainer)

    application_service = providers.Factory(
        ApplicationService,
        uow=repository_container.uow
    )
