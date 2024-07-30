from jwt import PyJWTError, ExpiredSignatureError, InvalidSignatureError
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from core.config.jwt import settings_bot
from src.admin.auth.service import auth_service


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        token = await auth_service.login(username, password)
        if token:
            request.session.update(**token.__dict__)
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        try:
            await auth_service.decode_token(token)
        except (ExpiredSignatureError, PyJWTError, InvalidSignatureError):
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings_bot.SECRET_KEY)
