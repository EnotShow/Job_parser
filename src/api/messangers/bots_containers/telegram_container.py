from dependency_injector import containers, providers

from src.api.messangers.bots_services.telegram_service import TelegramService


class TelegramServiceContainer(containers.DeclarativeContainer):

    telegram_service = providers.Factory(
        TelegramService
    )
