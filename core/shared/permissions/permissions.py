from starlette.requests import Request

from core.config.proj_settings import development_settings
from core.shared.permissions.BasePermission import BasePermission


class IsAuthenticated(BasePermission):
    @staticmethod
    async def is_permitted(request: Request, *args, **kwargs):
        return request.state.user is not None


class IsService(BasePermission):
    @staticmethod
    async def is_permitted(request: Request, *args, **kwargs):
        if request.headers.get('X-API-Key') == development_settings.service_api_token:
            return True
