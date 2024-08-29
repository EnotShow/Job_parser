from dependency_injector.wiring import inject
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.websockets import WebSocketDisconnect, WebSocket

from core.shared.connection_manager import ConnectionManager
from core.shared.permissions.permission_decorator import permission_required
from core.shared.permissions.permissions import IsAuthenticated, IsService
from src.api.smart_editor.errors import ProcesAlreadyRunningError, CacheBrokerConnectionError
from src.api.smart_editor.smart_dto import SmartEditorParamsDTO
from src.api.smart_editor.smart_service import SmartService

router = APIRouter()

socket_manager = ConnectionManager()


@router.get("/", status_code=status.HTTP_200_OK)
@permission_required([IsAuthenticated])
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

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Smart link creation failed")
    except ProcesAlreadyRunningError:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Smart creation already in progress")
    except CacheBrokerConnectionError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Cache broker connection error")


# TODO add websocket
@router.websocket("/ws")
async def get_smart_status(
    websocket: WebSocket,
):
    await socket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await socket_manager.send_personal_message(f"Received:{data}", websocket)
    except WebSocketDisconnect:
        socket_manager.disconnect(websocket)
        await socket_manager.send_personal_message("Bye!!!", websocket)
