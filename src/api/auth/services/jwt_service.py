import hashlib
from datetime import datetime, timedelta

from jwt import encode, get_unverified_header, decode, ExpiredSignatureError, PyJWTError, InvalidSignatureError

from core.config.jwt import JWTSettings, settings_bot
from src.api.auth.auth_dto import AccessTokenDTO, RefreshTokenDTO, TokenDTO, AccessTokenPayloadDTO, \
    RefreshTokenPayloadDTO
from src.api.users.user_dto import UserDTO, UserShortDTO


class JwtService:

    def __init__(self, config: JWTSettings):
        self.config = config

    async def create_tokens(self, dto: UserDTO) -> TokenDTO:
        access_token = await self.generate_access_token(dto)
        refresh_token = await self.generate_refresh_token(dto)
        return TokenDTO(access_token=access_token.access_token, refresh_token=refresh_token.refresh_token)

    async def encode_password(self, password: str) -> str:
        hash_object = hashlib.sha256()
        hash_object.update(password.encode())
        hash_password = hash_object.hexdigest()
        return hash_password

    async def generate_access_token(self, dto: UserDTO):
        expire = datetime.utcnow() + timedelta(seconds=self.config.ACCESS_TOKEN_LIFETIME)
        payload = AccessTokenPayloadDTO(
            token_type="access",
            user=UserShortDTO(id=dto.id, email=dto.email),
            is_admin=dto.is_admin,
            exp=expire,
            iat=datetime.utcnow(),

        )
        token = await self.encode_token(payload.model_dump())
        return AccessTokenDTO(access_token=token)

    async def generate_refresh_token(self, dto: UserDTO) -> RefreshTokenDTO:
        expire = datetime.utcnow() + timedelta(seconds=self.config.REFRESH_TOKEN_LIFETIME)
        payload = RefreshTokenPayloadDTO(
            token_type="refresh",
            user=UserShortDTO(id=dto.id, email=dto.email),
            exp=expire,
            iat=datetime.utcnow(),
        )
        token = await self.encode_token(payload.model_dump())
        return RefreshTokenDTO(refresh_token=token)

    async def encode_token(self, payload):
        return encode(payload, self.config.SECRET_KEY, algorithm="HS256")

    def _validate_token(self, token: str):
        token_info = get_unverified_header(token)
        if token_info["alg"] != self.config.ALGORITHM:
            raise InvalidSignatureError("Key error")
        return token

    async def decode_token(self, token: str) -> AccessTokenPayloadDTO | RefreshTokenPayloadDTO:
        try:
            self._validate_token(token)
            data = decode(token, self.config.SECRET_KEY, self.config.ALGORITHM)
            if data["token_type"] == "access":
                return AccessTokenPayloadDTO(**data)
            elif data["token_type"] == "refresh":
                return RefreshTokenPayloadDTO(**data)
        except ExpiredSignatureError:
            raise ExpiredSignatureError("Token lifetime is expired")
        except PyJWTError:
            raise Exception("Token is invalid")


jwt_service = JwtService(config=settings_bot)
