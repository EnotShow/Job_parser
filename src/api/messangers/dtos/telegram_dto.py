from typing import Optional

from core.shared.base_dto import BaseDTO


class TelegramPayloadDTO(BaseDTO):
    ref: Optional[int]
    login: Optional[bool]
