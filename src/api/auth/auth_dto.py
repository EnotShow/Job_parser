from datetime import datetime
from typing import Optional

from core.shared.base_dto import BaseDTO
from src.api.users.user_dto import UserShortDTO


class UserLoginDTO(BaseDTO):
    email: str
    password: str


class UserRegisterDTO(BaseDTO):
    email: str
    password: str
    language_code: str
    refer_id: int = 0


class ChangePasswordDTO(BaseDTO):
    old_password: str
    new_password: str


class AccessTokenDTO(BaseDTO):
    access_token: str


class RefreshTokenDTO(BaseDTO):
    refresh_token: str


class AccessTokenPayloadDTO(BaseDTO):
    token_type: str
    user: UserShortDTO
    exp: datetime
    iat: datetime


class RefreshTokenPayloadDTO(BaseDTO):
    token_type: str
    user: UserShortDTO
    exp: datetime
    iat: datetime


class TokenDTO(BaseDTO):
    access_token: str
    refresh_token: str


class AuthDTO(BaseDTO):
    email: AccessTokenDTO
    password: RefreshTokenDTO


class AuthHashDTO(BaseDTO):
    pk: Optional[str] = None
    user_id: Optional[int]
