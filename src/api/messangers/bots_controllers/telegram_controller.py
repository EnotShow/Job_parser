from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from src.api.messangers.bots_containers.telegram_container import TelegramServiceContainer
from src.api.messangers.bots_services.telegram_service import TelegramService
from src.api.messangers.dtos.telegram_dto import TelegramPayloadDTO

router = APIRouter(prefix="/telegram", tags=["Telegram"])


@router.post("/generate_payload", status_code=status.HTTP_200_OK)
@inject
async def generate_payload(
        data: TelegramPayloadDTO,
        telegram_service: TelegramService = Depends(Provide[TelegramServiceContainer.telegram_service])
):
    try:
        return await telegram_service.encode_payload(data)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'Unexpected error'})


@router.post("/connect_account", status_code=status.HTTP_200_OK)
@inject
async def send_payload(
        data: TelegramPayloadDTO,
        telegram_service: TelegramService = Depends(Provide[TelegramServiceContainer.telegram_service])
):
    try:
        return await telegram_service.send_payload(data)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, {'data': 'Unexpected error'})
