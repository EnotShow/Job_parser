from typing import List

from src.api.messangers.dtos.notification_dto import NotificationDTO
from src.client.BaseClient import BaseClient


class NotificationsClient(BaseClient):
    def __init__(self, client):
        self.client = client
        self.base_url = f"{self.client.base_url}/notifications"

    async def send_notification(self, data: NotificationDTO):
        await self.client.session.post(f"{self.base_url}/", json=data.model_dump())

    async def send_multiple_notifications(self, notifications_dto: List[NotificationDTO]):
        for notification_dto in notifications_dto:
            await self.send_notification(notification_dto)
