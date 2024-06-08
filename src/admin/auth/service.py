import hashlib
from datetime import datetime, timedelta

from jwt import encode, get_unverified_header, decode, ExpiredSignatureError, PyJWTError, InvalidSignatureError

from core.config.jwt import JWTSettings, settings_bot
from core.db.db_helper import db_helper
from src.admin.auth.dto import AccessTokenDTO
from src.api.dtos.user_dto import UserDTO
from src.api.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self, config: JWTSettings):
        self.config = config

    async def encode_password(self, password: str) -> str:
        hash_object = hashlib.sha256()
        hash_object.update(password.encode())
        hash_password = hash_object.hexdigest()
        return hash_password

    async def login(self, email: str, password: str) -> AccessTokenDTO:
        async with db_helper.get_db_session() as session:
            password = await self.encode_password(password)
            user = await UserRepository(session).get_by_email_password(email, password)
            if user:
                return await self.generate_access_token(user)

    async def generate_access_token(self, dto: UserDTO):
        expire = datetime.utcnow() + timedelta(seconds=self.config.ACCESS_TOKEN_LIFETIME)
        payload = {
            "token_type": "access",
            "user": {"user_id": str(dto.id), "user_email": str(dto.email)},
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        token = await self.encode_token(payload)
        return AccessTokenDTO(token=token)

    async def encode_token(self, payload):
        return encode(payload, self.config.SECRET_KEY, algorithm="HS256")

    def _validate_token(self, token: str):
        token_info = get_unverified_header(token)
        if token_info["alg"] != self.config.ALGORITHM:
            raise InvalidSignatureError("Key error")
        return token

    async def decode_token(self, token: str) -> dict:
        try:
            self._validate_token(token)
            return decode(token, self.config.SECRET_KEY, self.config.ALGORITHM)
        except ExpiredSignatureError:
            raise ExpiredSignatureError("Token lifetime is expired")
        except PyJWTError:
            raise Exception("Token is invalid")


auth_service = AuthService(config=settings_bot)
