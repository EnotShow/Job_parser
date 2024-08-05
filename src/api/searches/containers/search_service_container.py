from dependency_injector import containers, providers

from src.api.searches.containers.search_repository_container import SearchRepositoryContainer
from src.api.searches.searchings_service import SearchService


class SearchServiceContainer(containers.DeclarativeContainer):
    repository_container = providers.Container(SearchRepositoryContainer)

    search_service = providers.Factory(
        SearchService,
        repository=repository_container.search_repository,
    )