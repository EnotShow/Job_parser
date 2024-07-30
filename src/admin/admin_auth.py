from dependency_injector.wiring import Provide, inject
from jwt import PyJWTError, ExpiredSignatureError, InvalidSignatureError
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.api.containers.services_containers.auth_service_container import AuthServiceContainer
from src.api.services.auth_service import AuthService
from src.api.services.jwt_service import jwt_service

from core.config.jwt import settings_bot
from src.api.services.jwt_service import JwtService


class AdminAuth(AuthenticationBackend):
    @inject
    async def login(
            self,
            request: Request,
            auth_service: AuthService = Provide[AuthServiceContainer.auth_service],
    ) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        token = await auth_service.login(username, password)
        if token:
            request.session.update(**token.__dict__)
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(
            self,
            request: Request,
            jwt_service: JwtService = jwt_service,
    ) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        try:
            await jwt_service.decode_token(token)
        except (ExpiredSignatureError, PyJWTError, InvalidSignatureError):
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings_bot.SECRET_KEY)
