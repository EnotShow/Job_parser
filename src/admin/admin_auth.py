from dependency_injector.wiring import Provide, inject
from jwt import PyJWTError, ExpiredSignatureError, InvalidSignatureError
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from core.config.jwt import settings_bot
from src.api.auth.containers.auth_service_container import AuthServiceContainer
from src.api.auth.services.auth_service import AuthService
from src.api.auth.services.jwt_service import JwtService, jwt_service


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
            request.session.update({"token": token.access_token})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    @inject
    async def authenticate(
            self,
            request: Request,
            auth_service: AuthService = Provide[AuthServiceContainer.auth_service],
            jwt_service: JwtService = jwt_service,
    ) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        try:
            await auth_service.verify_access_token(token)
        except (ExpiredSignatureError, PyJWTError, InvalidSignatureError):
            try:
                token = await auth_service.refresh_access_token(token)
                request.session.update({"token": token.access_token})
            except (ExpiredSignatureError, PyJWTError, InvalidSignatureError):
                request.session.clear()
                return False

        token_data = await jwt_service.decode_token(token)
        if token_data.is_admin:
            return True


authentication_backend = AdminAuth(secret_key=settings_bot.SECRET_KEY)
