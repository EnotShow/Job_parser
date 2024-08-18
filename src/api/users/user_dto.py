from datetime import datetime
from typing import Optional

from core.shared.base_dto import BaseDTO


class UserDTO(BaseDTO):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
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
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    telegram_id: Optional[int] = None
    language_code: Optional[int] = None
    created_at: Optional[datetime] = None
    refer_id: Optional[int] = None


class UserUpdateDTO(BaseDTO):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    telegram_id: Optional[int] = None
    password: Optional[str] = None
    language_code: Optional[str] = None
    selected_language: Optional[str] = None
    paused: Optional[bool] = None
    links_limit: Optional[int] = None
    refer_id: Optional[int] = None


class UserSelfUpdateDTO(BaseDTO):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    selected_language: Optional[str] = None
    paused: Optional[bool] = None


class UserCreateDTO(BaseDTO):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    telegram_id: Optional[int] = None
    password: Optional[str] = None
    language_code: Optional[str] = None
    selected_language: Optional[str] = None
    refer_id: Optional[int] = None


class UserSettingsDTO(BaseDTO):
    user_id: int
    language_code: Optional[str]
    selected_language: Optional[str]
    paused: bool
    links_limit: Optional[int]
