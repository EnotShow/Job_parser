from typing import List, Union, Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from fastapi.exceptions import ResponseValidationError
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from core.shared.errors import NoRowsFoundError
from src.api.containers.services_containers import application_service_container
from src.api.containers.services_containers.application_service_container import ApplicationServiceContainer
from src.api.dtos.application_dto import ApplicationFilterDTO, ApplicationDTO, ApplicationCreateDTO
from src.api.services.application_service import ApplicationService

router = APIRouter(prefix="/application", tags=["application"])


@router.post("/find_multiple", status_code=status.HTTP_200_OK)
@inject
async def get_applications_if_exists(
        data: Union[ApplicationFilterDTO, List[ApplicationFilterDTO]],
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
) -> List[ApplicationDTO]:
    try:
        return await application_service.get_applications_if_exists(
            data if isinstance(data, list) else [data]
        )
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.post("/create_multiple", status_code=status.HTTP_200_OK)
@inject
async def get_applications_if_exists(
        data: Union[ApplicationFilterDTO, List[ApplicationFilterDTO]],
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
):
    try:
        return await application_service.create_multiple_applications(
            data if isinstance(data, list) else [data]
        )
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})