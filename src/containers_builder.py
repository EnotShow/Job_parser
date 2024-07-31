import src
from core.shared.async_session_container import AsyncSessionContainer
from src.api.auth.containers.auth_service_container import AuthServiceContainer
from src.api.messangers.bots_containers.notification_container import NotificationServiceContainer
from src.api.applications.containers.application_repository_container import ApplicationRepositoryContainer
from src.api.messangers.bots_containers.telegram_container import TelegramServiceContainer
from src.api.searches.containers.search_repository_container import SearchRepositoryContainer
from src.api.users.containers.user_repository_container import UserRepositoryContainer
from src.api.applications.containers.application_service_container import ApplicationServiceContainer
from src.api.searches.containers.search_service_container import SearchServiceContainer
from src.api.users.containers.user_service_container import UserServiceContainer

container_list = [
    AsyncSessionContainer,
    TelegramServiceContainer,
    NotificationServiceContainer,
    AuthServiceContainer,

    ApplicationRepositoryContainer,
    SearchRepositoryContainer,
    UserRepositoryContainer,

    UserServiceContainer,
    SearchServiceContainer,
    ApplicationServiceContainer,
]


def build_containers():
    for c in container_list:
        container = c()
        container.init_resources()
        container.wire(packages=[src])
