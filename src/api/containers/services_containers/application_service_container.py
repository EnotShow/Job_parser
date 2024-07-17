from dependency_injector import containers, providers

from src.api.containers.repositories_containers.application_repository_container import ApplicationRepositoryContainer
from src.api.services.application_service import ApplicationService


class ApplicationServiceContainer(containers.DeclarativeContainer):
    repository_container = providers.Container(ApplicationRepositoryContainer)

    application_service = providers.Factory(
        ApplicationService,
        repository=repository_container.application_repository,
    )