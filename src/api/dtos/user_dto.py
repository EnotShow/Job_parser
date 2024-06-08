from typing import Optional

from core.shared.base_dto import BaseDTO


class UserDTO(BaseDTO):
    id: int
    email: Optional[str]
    telegram_id: Optional[int]
    language_code: Optional[str]


class UserFilterDTO(BaseDTO):
    id: Optional[int] = None
    email: Optional[str] = None
    telegram_id: Optional[int] = None
    language_code: Optional[int] = None


class UserCreateDTO(BaseDTO):
    email: Optional[str]
    telegram_id: Optional[int]
    password: Optional[str]
    language_code: str
