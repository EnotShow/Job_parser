from dependency_injector import containers, providers

from core.db.db_helper import db_helper
from core.shared.async_session_container import AsyncSessionContainer
from src.api.repositories.searchings_repository import SearchRepository


class SearchRepositoryContainer(containers.DeclarativeContainer):
    db_session_container = providers.Container(AsyncSessionContainer)

    search_repository = providers.Factory(
        SearchRepository,
        db_session=db_session_container.db_session,
    )
