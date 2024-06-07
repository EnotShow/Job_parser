from dependency_injector import containers, providers

from src.api.containers.repositories_containers.search_repository_container import SearchRepositoryContainer
from src.api.containers.repositories_containers.user_repository_container import UserRepositoryContainer
from src.api.services.searchings_service import SearchService
from src.api.services.user_service import UserService


class SearchServiceContainer(containers.DeclarativeContainer):
    repository_container = providers.Container(SearchRepositoryContainer)

    search_service = providers.Factory(
        SearchService,
        repository=repository_container.search_repository,
    )