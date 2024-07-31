from http.client import HTTPException

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.auth.services.jwt_service import jwt_service


class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, jwt_service=jwt_service):
        super().__init__(app)
        self._jwt_service = jwt_service

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        request.state.user = None
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                scheme, token = auth_header.split()
                if scheme.lower() == 'bearer':
                    user_info = await self._jwt_service.decode_token(token)
                    request.state.user = user_info

            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
