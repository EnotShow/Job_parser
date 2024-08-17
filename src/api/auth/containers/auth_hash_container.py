from dependency_injector import containers, providers

from core.config.db import settings_broker
from src.api.auth.auth_repository import AuthHashRepository


class AuthHashRepositoryContainer(containers.DeclarativeContainer):
    db_settings = settings_broker.broker_url

    auth_hash_repository = providers.Factory(
        AuthHashRepository
    )
