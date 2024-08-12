from typing import List, Union
from httpx import Response

from src.api.messangers.dtos.notification_dto import NotificationDTO
from src.client.BaseClient import BaseClient


class NotificationsClient(BaseClient):
    def __init__(self, client):
        self.client = client
        self.session = client.session
        self.base_url = f"{self.client.base_url}/notifications"

    async def send_notification(
        self, data: NotificationDTO, *, return_response: bool = False
    ) -> Union[None, Response]:
        response = await self.session.post(f"{self.base_url}/", json=data.model_dump())
        if return_response:
            return response

    async def send_multiple_notifications(
        self, notifications_dto: List[NotificationDTO], *, return_response: bool = False
    ) -> Union[List[Response], None]:
        responses = []
        for notification_dto in notifications_dto:
            response = await self.send_notification(notification_dto, return_response=True)
            if return_response:
                responses.append(response)
        if return_response:
            return responses
