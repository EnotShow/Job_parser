from typing import List, Union

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.requests import Request

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No rows found")


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No rows found")


@router.put("/{application_id}", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def update_application(
        application_id: int,
        data: ApplicationUpdateDTO,
        request: Request,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
) -> ApplicationDTO:
    try:
        data.id = application_id
        return await application_service.update_application(data)
    except NoRowsFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No rows found")


@router.post("/", status_code=status.HTTP_201_CREATED)
@permission_required([IsService])
@inject
async def create_application(
        data: ApplicationCreateDTO,
        request: Request,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
) -> ApplicationFullDTO:
    try:
        return await application_service.create_application(data)
    except NoRowsFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No rows found")


@router.post("/find_multiple", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def get_applications_if_exists(
        data: Union[ApplicationFilterDTO, List[ApplicationFilterDTO]],
        request: Request,
        limit: int = 10,
        page: int = 1,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
) -> List[ApplicationDTO]:
    try:
        return await application_service.get_applications_if_exists(
            data if isinstance(data, list) else [data],
        )
    except NoRowsFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No rows found")


@router.post("/create_multiple", status_code=status.HTTP_201_CREATED)
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No rows found")
