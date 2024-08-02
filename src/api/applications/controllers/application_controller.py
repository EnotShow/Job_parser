from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from core.shared.errors import NoRowsFoundError
from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsAuthenticated
from src.api.applications.application_dto import ApplicationUpdateDTO
from src.api.applications.application_service import ApplicationService
from src.api.applications.containers.application_service_container import ApplicationServiceContainer

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_user_applications(
        request: Request,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
        limit: int = 10,
        page: int = 1
):
    try:
        return await application_service.get_user_applications(
            request.state.user['user']['user_id'],
            limit=limit,
            page=page
        )
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.get("/{application_id}", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_user_applied_applications(
        application_id: int,
        request: Request,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
):
    try:
        return await application_service.get_user_application(request.state.token.user.id, application_id)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.put("/{application_id}", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def update_user_application(
        application_id: int,
        data: ApplicationUpdateDTO,
        request: Request,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
):
    try:
        data.id = application_id
        return await application_service.update_user_application(data, request.state.token.user.id)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.get("/applied/", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_user_applied_applications(
        user_id: int,
        request: Request,
        limit: int = 10,
        page: int = 1,
        application_service: ApplicationService = Depends(Provide[ApplicationServiceContainer.application_service]),
):
    try:
        return await application_service.get_user_applied_applications(request.state.token.user.id, limit=limit, page=page)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})
