from typing import Optional

from core.shared.base_dto import BaseDTO


class TelegramPayloadDTO(BaseDTO):
    ref: Optional[int] = None
    login: Optional[bool] = None
    connect: Optional[bool] = None
    user_id: Optional[int] = None
