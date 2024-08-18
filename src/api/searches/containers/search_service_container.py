from dependency_injector import containers, providers

from core.shared.async_session_container import UnitOfWorkContainer
from src.api.searches.searchings_service import SearchService


class SearchServiceContainer(containers.DeclarativeContainer):
    uow = providers.Container(UnitOfWorkContainer)

    search_service = providers.Factory(
        SearchService,
        uow=uow.uow
    )
