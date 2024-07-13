from dependency_injector import containers, providers

from src.api.services.bots_services.notification_service import NotificationService


class NotificationServiceContainer(containers.DeclarativeContainer):

    notification_service = providers.Factory(
        NotificationService
    )
