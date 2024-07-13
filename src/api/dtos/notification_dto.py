from pydantic import BaseModel

from core.shared.enums import SocialNetworkEnum
from src.api.dtos.application_dto import ApplicationCreateDTO


class NotificationDTO(BaseModel):
    """
    owner_id - id of owner user
    social_network - selected by owner social network to send notification
    social_network_id - id on selected by owner social network
    message: str
    """
    owner_id: int
    social_network: SocialNetworkEnum = SocialNetworkEnum.telegram
    social_network_id: str
    message: str


class NotificationControllerDTO(BaseModel):
    application: ApplicationCreateDTO
    notification: NotificationDTO
