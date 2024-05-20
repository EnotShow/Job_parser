from typing import Annotated

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

from src.api.dependencies.ISearchRepository import ISearchRepository
from src.api.services.search_service import SearchService


class ISearchContainer(containers.DeclarativeContainer):

    search_service = providers.Factory(
        SearchService, search_repository=providers.Resource(ISearchRepository)
    )


ISearchService = Annotated[SearchService, Provide[ISearchContainer.search_service]]