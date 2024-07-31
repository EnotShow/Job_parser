from pydantic import BaseModel

from core.shared.enums import SocialNetworkEnum


class NotificationDTO(BaseModel):
    """
    owner_id - id of owner user
    social_network - selected by owner social network to send notification
    social_network_id - id on selected by owner social network
    message: str
    """
    owner_id: int
    social_network: SocialNetworkEnum = SocialNetworkEnum.telegram
    social_network_id: int
    message: str
