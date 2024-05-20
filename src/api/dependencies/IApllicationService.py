from typing import Annotated

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

from src.api.dependencies.IApplicationRepository import IApplicationRepository
from src.api.services.application_service import ApplicationService


class IApplicationContainer(containers.DeclarativeContainer):

    application_service = providers.Factory(
        ApplicationService, application_repository=providers.Resource(IApplicationRepository)
    )


IApplicationService = Annotated[ApplicationService, Provide[IApplicationContainer.application_service]]