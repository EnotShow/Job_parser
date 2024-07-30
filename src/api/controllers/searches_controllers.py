from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from core.shared.errors import NoRowsFoundError
from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsAuthenticated, IsService
from src.api.containers.services_containers.search_service_container import SearchServiceContainer
from src.api.dtos.pagination_dto import PaginationDTO
from src.api.dtos.search_dto import SearchDTO, SearchCreateDTO, SearchUpdateDTO
from src.api.services.searchings_service import SearchService

router = APIRouter(prefix="/searches", tags=["searches"])


@router.get("/", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def get_all_searches(
        request: Request,
        limit: int = 10,
        page: int = 1,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
) -> PaginationDTO[SearchDTO]:
    try:
        return await search_service.get_all_searches(limit, page)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.get("/user_searches", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_user_searches(
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
        limit: int = 10,
        page: int = 1
):
    try:
        return await search_service.get_user_searches(request.state.token.user.id, limit, page)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.get("/{id}", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def get_search(
        id: int,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
) -> SearchDTO:
    try:
        return await search_service.get_search(id)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.get("/user_search/{search_id}", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_user_search(
        search_id: int,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
):
    try:
        return await search_service.get_user_search(request.state.token.user.id, search_id)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.post("/", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def create_search(
        data: SearchDTO,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
):
    try:
        return await search_service.create_search(data)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.post("/user_search", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def create_user_search(
        data: SearchCreateDTO,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
):
    try:
        return await search_service.create_user_search(data, request.state.token.user.id)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.delete("/{id}", status_code=status.HTTP_200_OK)
@permission_required([IsService])
@inject
async def delete_search(
        id: int,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
):
    try:
        return await search_service.delete_search(id)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.delete("/user_search/{search_id}", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def delete_user_search(
        search_id: int,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
):
    try:
        return await search_service.delete_user_search(request.state.token.user.id, search_id)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.put("/user_search/{search_id}", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def update_user_search(
        search_id: int,
        data: SearchUpdateDTO,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
):
    try:
        return await search_service.update_user_search(data, request.state.token.user.id)
    except NoRowsFoundError:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'No rows found'})
