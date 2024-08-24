from dependency_injector.wiring import inject
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.shared.errors import NoRowsFoundError
from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsAuthenticated
from src.api.smart_editor.smart_dto import SmartEditorParamsDTO
from src.api.smart_editor.smart_service import SmartService

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
@inject
async def get_smart(
        smart_dto: SmartEditorParamsDTO,
        request: Request,
        smart_service: SmartService = Depends(),
):
    try:
        if smart_dto.owner_id != request.user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not match")

        is_processing = smart_service.smart_links_create(smart_dto)

        if is_processing:
            return JSONResponse(
                content={"details": "Smart link creation processing, we will inform you after the process is complete"},
                status_code=status.HTTP_202_ACCEPTED
            )

        return {"details": "Smart link creation failed"}
    except NoRowsFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No rows found")
