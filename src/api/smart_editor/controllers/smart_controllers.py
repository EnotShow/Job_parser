from dependency_injector.wiring import inject
from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.requests import Request

from core.shared.errors import NoRowsFoundError
from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsAuthenticated

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_smart(
        request: Request,
):
    try:
        pass
    except NoRowsFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No rows found")
