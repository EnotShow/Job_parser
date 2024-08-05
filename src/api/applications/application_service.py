from typing import List
from uuid import UUID

from dependency_injector.wiring import inject, Provide

from core.db.uow import UnitOfWork
from core.shared.async_session_container import UnitOfWorkContainer
from core.shared.base_service import BaseService
from core.shared.errors import NoRowsFoundError
from src.api.applications.application_dto import ApplicationCreateDTO, ApplicationDTO, ApplicationFilterDTO, \
    ApplicationUpdateDTO, ApplicationFullDTO
from src.api.applications.application_repository import ApplicationRepository
from src.api.middleware.dtos.pagination_dto import PaginationDTO


class ApplicationService(BaseService):

    @inject
    def __init__(self, uow: UnitOfWork = Provide[UnitOfWorkContainer.uow]):
        self.uow = uow

    async def get_all_applications(self, limit: int = 10, page: int = 1) -> PaginationDTO[ApplicationDTO]:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            response_objects = await repository.get(limit=limit, page=page)
            return self._paginate(response_objects, page, len(response_objects))

    async def get_application(self, id: int) -> ApplicationDTO:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            try:
                return await repository.get_single(id)
            except NoRowsFoundError:
                raise NoRowsFoundError

    async def get_application_by_url(self, url: str) -> ApplicationDTO:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            try:
                filter = ApplicationFilterDTO(url=url)
                response = await repository.get_filtered(filter, limit=1, page=1)
                return response[0]
            except NoRowsFoundError:
                raise NoRowsFoundError

    async def get_application_by_short_id(self, short_id: UUID) -> ApplicationDTO:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            try:
                filter = ApplicationFilterDTO(short_id=short_id)
                response = await repository.get_filtered(filter, limit=1, page=1)
                return response[0]
            except NoRowsFoundError:
                raise NoRowsFoundError

    async def get_user_applications(self, user_id: int, limit: int = 10, page: int = 1) -> PaginationDTO[ApplicationDTO]:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            try:
                filter = ApplicationFilterDTO(owner_id=user_id)
                response_objects = await repository.get_filtered(filter, limit=limit, page=page)
                total = await repository.get_count(filter)
                return self._paginate(response_objects, page, len(response_objects), total)
            except NoRowsFoundError:
                raise NoRowsFoundError

    async def get_user_application(self, user_id: int, application_id: int) -> ApplicationDTO:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            try:
                filter = ApplicationFilterDTO(owner_id=user_id, id=application_id)
                response = await repository.get_filtered(filter, limit=1, page=1)
                return response[0]
            except NoRowsFoundError:
                raise NoRowsFoundError(f"Application {application_id} not found")

    async def get_user_applied_applications(self, user_id: int, limit: int = 10, page: int = 1) -> PaginationDTO[ApplicationDTO]:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            try:
                filter = ApplicationFilterDTO(applied=True, owner_id=user_id)
                response_objects = await repository.get_filtered(filter, limit=limit, page=page)
                return self._paginate(response_objects, page, len(response_objects))
            except NoRowsFoundError:
                raise NoRowsFoundError

    async def get_applications_if_exists(self, filters: List[ApplicationFilterDTO], limit: int = 10, page: int = 1) -> PaginationDTO[ApplicationDTO]:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            try:
                response_objects = await repository.get_filtered_multiple_applications(filters, limit=limit, page=page)
                return self._paginate(response_objects, page, len(response_objects))
            except NoRowsFoundError:
                raise NoRowsFoundError

    async def get_applications_by_user_id(self, user_id: int, limit: int = 10, page: int = 1) -> PaginationDTO[ApplicationDTO]:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            try:
                filter = ApplicationFilterDTO(user_id=user_id)
                response_objects = await repository.get_filtered(filter, limit=limit, page=page)
                return self._paginate(response_objects, page, len(response_objects))
            except NoRowsFoundError:
                raise NoRowsFoundError

    async def get_applications_by_telegram_id(self, telegram_id: int, limit: int = 10, page: int = 1) -> PaginationDTO[ApplicationDTO]:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            try:
                filter = ApplicationFilterDTO(telegram_id=telegram_id)
                response_objects = await repository.get_filtered(filter, limit=limit, page=page)
                return self._paginate(response_objects, page, len(response_objects))
            except NoRowsFoundError:
                raise NoRowsFoundError

    async def create_application(self, dto: ApplicationCreateDTO) -> ApplicationFullDTO:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            try:
                return await repository.create(dto)
            except Exception as e:
                raise e

    async def create_multiple_applications(self, dtos: List[ApplicationCreateDTO]) -> List[ApplicationFullDTO]:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            try:
                return await repository.create_multiple(dtos)
            except Exception as e:
                raise e

    async def update_application(self, dto: ApplicationUpdateDTO) -> ApplicationDTO:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            return await repository.update(dto)

    async def update_user_application(self, dto: ApplicationUpdateDTO, user_id: int) -> ApplicationDTO:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            application = await repository.get_single(dto.id)
            if application and application.owner_id == user_id:
                return await repository.update(dto)
            else:
                raise NoRowsFoundError(f"Application {dto.id} not found")

    async def delete_application(self, id: int) -> None:
        async with self.uow as uow:
            repository = ApplicationRepository(uow)
            return await repository.delete(id)