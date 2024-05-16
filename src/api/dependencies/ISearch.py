from typing import Annotated

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

from core.db.db_helper import db_helper
from src.api.services.search_service import SearchService
from src.repositories.searchings_repository import SearchRepository


class ISearchContainer(containers.DeclarativeContainer):
    search_repository = providers.Factory(
        SearchRepository, db_session=providers.Resource(db_helper.get_db_session)
    )

    search_service = providers.Factory(
        SearchService, search_repository=providers.Resource(search_repository)
    )


ISearchRepository = Annotated[SearchRepository, Provide[ISearchContainer.search_repository]]
ISearchService = Annotated[SearchService, Provide[ISearchContainer.search_service]]
