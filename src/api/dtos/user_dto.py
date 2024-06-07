from typing import Optional

from core.shared.base_dto import BaseDTO


class UserDTO(BaseDTO):
    id: int
    email: Optional[str]
    telegram_id: Optional[str]
    language_code: Optional[int]


class UserCreateDTO(BaseDTO):
    email: Optional[str]
    telegram_id: Optional[int]
    language_code: str
