from typing import List, Union

from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import NoResultFound

from core.shared.errors import NoRowsFoundError
from src.api.containers.repositories_containers.application_repository_container import ApplicationRepositoryContainer
from src.api.dtos.application_dto import ApplicationCreateDTO, ApplicationDTO, ApplicationFilterDTO, \
    ApplicationUpdateDTO
from src.api.repositories.application_repository import ApplicationRepository


class ApplicationService:

    @inject
    def __init__(self,
                 repository: ApplicationRepository = Provide[ApplicationRepositoryContainer.application_repository]):
        self._repository = repository

    async def get_all_applications(self):
        return await self._repository.get()

    async def get_application(self, id: int):
        try:
            return await self._repository.get_single(id)
        except Exception as e:
            return None

    async def get_application_by_url(self, url: str):
        try:
            filter = ApplicationFilterDTO(url=url)
            return await self._repository.get_filtered(filter, get_single=True)
        except Exception as e:
            return None

    async def get_applications_if_exists(self, filters: List[ApplicationFilterDTO]):
        try:
            return await self._repository.get_filtered_multiple_applications(filters)
        except (NoResultFound, AttributeError) as e:
            return NoRowsFoundError

    async def get_applications_by_user_id(self, user_id: int):
        try:
            filter = ApplicationFilterDTO(user_id=user_id)
            return await self._repository.get_filtered(filter, get_single=False)
        except Exception as e:
            return None

    async def get_applications_by_telegram_id(self, telegram_id: int, count: bool = False):
        try:
            filter = ApplicationFilterDTO(telegram_id=telegram_id)
            if count:
                return await self._repository.get_filtered(filter, get_single=False, count=True)
            return await self._repository.get_filtered(filter, get_single=False)
        except Exception as e:
            return None

    async def create_application(self, dto: ApplicationCreateDTO):
        try:
            return await self._repository.create(dto)
        except Exception as e:
            return None

    async def create_multiple_applications(self, dtos: List[ApplicationCreateDTO]):
        try:
            return await self._repository.create_multiple(dtos)
        except Exception as e:
            return None

    async def update_application(self, dto: ApplicationUpdateDTO):
        return await self._repository.update(dto)

    async def delete_application(self, id: int):
        return await self._repository.delete(id)
