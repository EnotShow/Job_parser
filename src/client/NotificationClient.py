from typing import List, Union
from httpx import Response

from src.api.messangers.dtos.notification_dto import MessangerNotificationDTO
from src.client.BaseClient import BaseClient


class NotificationsClient(BaseClient):
    def __init__(self, client):
        self.client = client
        self.session = client.session
        self.base_url = f"{self.client.base_url}/notifications"

    async def send_notification(
        self, data: MessangerNotificationDTO, *, return_response: bool = False
    ) -> Union[None, Response]:
        response = await self.session.post(f"{self.base_url}/notify", json=data.model_dump())
        if return_response:
            return response

    async def send_multiple_notifications(
        self, notifications_dto: List[MessangerNotificationDTO], *, return_response: bool = False
    ) -> Union[List[Response], None]:
        data_to_send = [notification_dto.model_dump() for notification_dto in notifications_dto]
        response = await self.session.post(f"{self.base_url}/notify_multiple", json=data_to_send)
        if return_response:
            return response
