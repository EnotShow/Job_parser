import src
from core.shared.async_session_container import AsyncSessionContainer
from src.api.containers.repositories_containers.application_repository_container import ApplicationRepositoryContainer
from src.api.containers.repositories_containers.search_repository_container import SearchRepositoryContainer
from src.api.containers.repositories_containers.user_repository_container import UserRepositoryContainer

container_list = [
    AsyncSessionContainer,
    ApplicationRepositoryContainer,
    SearchRepositoryContainer,
    UserRepositoryContainer,
]


def build_containers():
    for c in container_list:
        container = c()
        container.init_resources()
        container.wire(packages=[src])
