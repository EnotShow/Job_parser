from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from core.shared.errors import NoRowsFoundError
from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsService
from src.api.middleware.dtos.pagination_dto import PaginationDTO
from src.api.searches.containers.search_service_container import SearchServiceContainer
from src.api.searches.search_dto import SearchDTO
from src.api.searches.searchings_service import SearchService

router = APIRouter(prefix="/service")


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


@router.post("/", status_code=status.HTTP_201_CREATED)
@permission_required([IsService])
@inject
async def create_search(
        data: SearchDTO,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
) -> SearchDTO:
    try:
        return await search_service.create_search(data)
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
