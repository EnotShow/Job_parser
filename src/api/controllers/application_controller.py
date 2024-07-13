from datetime import datetime
from typing import List, Union
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.responses import RedirectResponse
from starlette.status import HTTP_400_BAD_REQUEST

from core.shared.errors import NoRowsFoundError
from src.api.containers.services_containers.application_service_container import ApplicationServiceContainer
from src.api.dtos.application_dto import ApplicationFilterDTO, ApplicationDTO, ApplicationCreateDTO, \
    ApplicationUpdateDTO
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
async def create_multiple_applications(
        data: Union[ApplicationFilterDTO, List[ApplicationFilterDTO]],
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
):
    try:
        return await application_service.create_multiple_applications(
            data if isinstance(data, list) else [data]
        )
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.post("/user_applications", status_code=status.HTTP_201_CREATED)
@inject
async def get_user_applied_applications(
        data: ApplicationCreateDTO,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
):
    try:
        return await application_service.create_application(data)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.get("/user_application/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_applied_applications(
        user_id: int,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
):
    try:
        return await application_service.get_user_applied_applications(user_id)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.post("/{short_id}", status_code=status.HTTP_301_MOVED_PERMANENTLY)
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
