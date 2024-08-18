from src.api.messangers.dtos.telegram_dto import TelegramPayloadDTO
from src.client.BaseClient import BaseClient


class TelegramClient(BaseClient):
    def __init__(self, client):
        self.client = client
        self.session = client.session
        self.base_url = f"{self.client.base_url}/telegram"

    async def generate_payload(self, data: TelegramPayloadDTO, *, return_response: bool = False) -> dict:
        response = await self.session.post(f"{self.base_url}/generate_payload", json=data.dict())
        if return_response:
            return response
        return response.json()
