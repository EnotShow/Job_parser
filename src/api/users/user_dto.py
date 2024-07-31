from datetime import datetime
from typing import Optional

from core.shared.base_dto import BaseDTO


class UserDTO(BaseDTO):
    id: int
    email: Optional[str]
    telegram_id: Optional[int]
    language_code: Optional[str]
    selected_language: Optional[str]
    created_at: Optional[datetime]


class UserShortDTO(BaseDTO):
    id: int
    email: Optional[str]


class UserFilterDTO(BaseDTO):
    id: Optional[int] = None
    email: Optional[str] = None
    telegram_id: Optional[int] = None
    language_code: Optional[int] = None
    created_at: Optional[datetime] = None
    refer_id: Optional[int] = None


class UserUpdateDTO(BaseDTO):
    id: int
    email: Optional[str] = None
    telegram_id: Optional[int] = None
    password: Optional[str] = None
    language_code: Optional[int] = None
    selected_language: Optional[str] = None
    paused: Optional[bool] = None
    links_limit: Optional[int] = None


class UserCreateDTO(BaseDTO):
    email: Optional[str] = None
    telegram_id: Optional[int] = None
    password: Optional[str] = None
    language_code: Optional[str] = None
    selected_language: Optional[str] = None
    refer_id: Optional[int] = None


class UserSettingsDTO(BaseDTO):
    id: int
    language_code: Optional[str]
    selected_language: Optional[str]
    paused: bool
    links_limit: Optional[int]
