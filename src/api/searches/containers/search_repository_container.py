from dependency_injector import containers, providers

from core.shared.async_session_container import AsyncSessionContainer
from src.api.searches.searchings_repository import SearchRepository


class SearchRepositoryContainer(containers.DeclarativeContainer):
    db_session_container = providers.Container(AsyncSessionContainer)

    search_repository = providers.Factory(
        SearchRepository,
        db_session=db_session_container.db_session,
    )
