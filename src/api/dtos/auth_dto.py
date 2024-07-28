from core.shared.base_dto import BaseDTO


class AccessTokenDTO(BaseDTO):
    token: str


class RefreshTokenDTO(BaseDTO):
    token: str


class TokenDTO(BaseDTO):
    access_token: str
    refresh_token: str


class AuthDTO(BaseDTO):
    email: AccessTokenDTO
    password: RefreshTokenDTO
