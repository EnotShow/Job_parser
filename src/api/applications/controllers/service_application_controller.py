from datetime import datetime
from typing import List, Union
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_400_BAD_REQUEST

from core.shared.errors import NoRowsFoundError
from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsService
from src.api.applications.application_dto import ApplicationFilterDTO, ApplicationDTO, ApplicationUpdateDTO, \
    ApplicationCreateDTO, ApplicationFullDTO
from src.api.applications.application_service import ApplicationService
from src.api.applications.containers.application_service_container import ApplicationServiceContainer
from src.api.middleware.dtos.pagination_dto import PaginationDTO

router = APIRouter(prefix="/service")


@router.get("/", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def get_all_applications(
        request: Request,
        limit: int = 10,
        page: int = 1,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
) -> PaginationDTO[ApplicationDTO]:
    try:
        return await application_service.get_all_applications(limit=limit, page=page)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.get("/{id}", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def get_application(
        id: int,
        request: Request,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
) -> ApplicationDTO:
    try:
        return await application_service.get_application(id)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.put("/", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def update_application(
        data: ApplicationUpdateDTO,
        request: Request,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
):
    try:
        return await application_service.update_application(data)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.post("/", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def create_application(
        data: ApplicationCreateDTO,
        request: Request,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
):
    try:
        return await application_service.create_application(data)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.post("/find_multiple", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def get_applications_if_exists(
        data: Union[ApplicationFilterDTO, List[ApplicationFilterDTO]],
        request: Request,
        limit: int = 10,
        page: int = 1,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
) -> PaginationDTO[ApplicationDTO]:
    try:
        return await application_service.get_applications_if_exists(
            data if isinstance(data, list) else [data],
            limit=limit,
            page=page
        )
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.post("/create_multiple", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def create_multiple_applications(
        data: Union[ApplicationFilterDTO, List[ApplicationFilterDTO]],
        request: Request,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
) -> List[ApplicationFullDTO]:
    try:
        return await application_service.create_multiple_applications(
            data if isinstance(data, list) else [data]
        )
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.get("/{short_id}", status_code=status.HTTP_301_MOVED_PERMANENTLY)
@inject
async def redirect_to_application(
        short_id: UUID,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
):
    try:
        application = await application_service.get_application_by_short_id(short_id)

        if application is None:
            raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})

        if not application.applied:
            updated_dto = ApplicationUpdateDTO(
                id=application.id,
                applied=True,
                applied_at=datetime.utcnow()
            )
            await application_service.update_application(updated_dto)

        return RedirectResponse(url=application.url, status_code=status.HTTP_301_MOVED_PERMANENTLY)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})