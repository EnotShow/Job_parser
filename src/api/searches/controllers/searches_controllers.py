from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.requests import Request

from core.shared.errors import NoRowsFoundError
from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsAuthenticated
from src.api.middleware.dtos.pagination_dto import PaginationDTO
from src.api.searches.containers.search_service_container import SearchServiceContainer
from src.api.searches.search_dto import SearchCreateDTO, SearchUpdateDTO, SearchDTO
from src.api.searches.searchings_service import SearchService

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_user_searches(
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
        limit: int = 10,
        page: int = 1
) -> PaginationDTO[SearchDTO]:
    try:
        return await search_service.get_user_searches(request.state.token.user.id, limit, page)
    except NoRowsFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No rows found")


@router.get("/{search_id}", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_user_search(
        search_id: int,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
) -> SearchDTO:
    try:
        return await search_service.get_user_search(request.state.token.user.id, search_id)
    except NoRowsFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No rows found")


@router.post("/", status_code=status.HTTP_201_CREATED)
@permission_required([IsAuthenticated])
@inject
async def create_user_search(
        data: SearchCreateDTO,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
) -> SearchDTO:
    try:
        return await search_service.create_user_search(data, request.state.token.user.id)
    except NoRowsFoundError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'data': 'No rows found'})


@router.post("/create_multiple", status_code=status.HTTP_201_CREATED)
@permission_required([IsAuthenticated])
@inject
async def create_multiple_searches(
        data: list[SearchCreateDTO],
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
):
    try:
        # Check if user id matches
        for search in data:
            if search.user_id != request.state.token.user.id:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User id does not match")
        return await search_service.create_multiple_searches(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{search_id}", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def delete_user_search(
        search_id: int,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
):
    try:
        await search_service.delete_user_search(search_id, request.state.token.user.id)
        return {"detail": "Search deleted successfully"}
    except NoRowsFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No rows found")


@router.put("/{search_id}", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def update_user_search(
        search_id: int,
        data: SearchUpdateDTO,
        request: Request,
        search_service: SearchService = Depends(Provide[SearchServiceContainer.search_service]),
) -> SearchDTO:
    try:
        data.id = search_id
        return await search_service.update_user_search(data, request.state.token.user.id)
    except NoRowsFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No rows found")
