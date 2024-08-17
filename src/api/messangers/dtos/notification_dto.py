from typing import Optional

from pydantic import BaseModel

from core.shared.enums import SocialNetworkEnum


class MessangerNotificationDTO(BaseModel):
    """
    owner_id - id of owner user
    social_network - selected by owner social network to send notification
    social_network_id - id on selected by owner social network
    message: str
    search_title: Optional[str] = None
    application_id: Optional[int] = None
    language: Optional[str] = None
    """
    owner_id: int
    social_network: SocialNetworkEnum = SocialNetworkEnum.telegram
    social_network_id: int
    message: str
    search_title: Optional[str] = None
    application_id: Optional[int] = None
    language: Optional[str] = None
