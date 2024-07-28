from typing import List, Union
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import NoResultFound

from core.shared.base_service import BaseService
from core.shared.errors import NoRowsFoundError
from src.api.containers.repositories_containers.application_repository_container import ApplicationRepositoryContainer
from src.api.dtos.application_dto import ApplicationCreateDTO, ApplicationDTO, ApplicationFilterDTO, \
    ApplicationUpdateDTO, ApplicationFullDTO
from src.api.dtos.pagination_dto import PaginationDTO
from src.api.repositories.application_repository import ApplicationRepository


class ApplicationService(BaseService):

    @inject
    def __init__(self,
                 repository: ApplicationRepository = Provide[ApplicationRepositoryContainer.application_repository]):
        self._repository = repository

    async def get_all_applications(self, limit: int = 10, page: int = 1) -> PaginationDTO[ApplicationDTO]:
        response_objects = await self._repository.get(limit=limit, page=page)
        return self._paginate(response_objects, page, len(response_objects))

    async def get_application(self, id: int) -> ApplicationDTO:
        try:
            return await self._repository.get_single(id)
        except Exception as e:
            raise NoRowsFoundError

    async def get_application_by_url(self, url: str) -> ApplicationDTO:
        try:
            filter = ApplicationFilterDTO(url=url)
            return await self._repository.get_filtered(filter, limit=1, page=1)
        except Exception as e:
            raise NoRowsFoundError

    async def get_application_by_short_id(self, short_id: UUID) -> ApplicationDTO:
        try:
            filter = ApplicationFilterDTO(short_id=short_id)
            return await self._repository.get_filtered(filter)
        except Exception as e:
            raise NoRowsFoundError

    async def get_user_applied_applications(self, user_id: int, limit: int = 10, page: int = 1
                                            ) -> PaginationDTO[ApplicationDTO]:
        try:
            filter = ApplicationFilterDTO(applied=True, owner_id=user_id)
            return await self._repository.get_filtered(filter, limit=limit, page=page)
        except Exception as e:
            raise NoRowsFoundError

    async def get_applications_if_exists(self, filters: List[ApplicationFilterDTO], limit: int = 10, page: int = 1
                                         ) -> PaginationDTO[ApplicationDTO]:
        try:
            response_objects = await self._repository.get_filtered_multiple_applications(filters, limit=limit, page=page)
            return self._paginate(response_objects, page, len(response_objects))
        except (NoResultFound, AttributeError) as e:
            raise NoRowsFoundError

    async def get_applications_by_user_id(self, user_id: int, limit: int = 10, page: int = 1
                                          ) -> PaginationDTO[ApplicationDTO]:
        try:
            filter = ApplicationFilterDTO(user_id=user_id)
            response_objects = await self._repository.get_filtered(filter, limit=limit, page=page)
            return self._paginate(response_objects, page, len(response_objects))
        except Exception as e:
            raise NoRowsFoundError

    async def get_applications_by_telegram_id(self, telegram_id: int, limit: int = 10, page: int = 1
                                              ) -> PaginationDTO[ApplicationDTO]:
        try:
            filter = ApplicationFilterDTO(telegram_id=telegram_id)
            response_objects = await self._repository.get_filtered(filter, limit=limit, page=page)
            return self._paginate(response_objects, page, len(response_objects))
        except Exception as e:
            raise NoRowsFoundError

    async def create_application(self, dto: ApplicationCreateDTO) -> ApplicationFullDTO:
        try:
            return await self._repository.create(dto)
        except Exception as e:
            raise e

    async def create_multiple_applications(self, dtos: List[ApplicationCreateDTO]) -> List[ApplicationFullDTO]:
        try:
            return await self._repository.create_multiple(dtos)
        except Exception as e:
            raise e

    async def update_application(self, dto: ApplicationUpdateDTO) -> ApplicationDTO:
        return await self._repository.update(dto)

    async def delete_application(self, id: int) -> None:
        return await self._repository.delete(id)
