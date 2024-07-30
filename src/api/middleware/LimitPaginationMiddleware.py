from typing import Optional
from urllib.parse import urlencode

from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, JSONResponse


class LimitPaginationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, max_limit: int):
        super().__init__(app)
        self.max_limit = max_limit

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        query_params = dict(request.query_params)

        limit: Optional[str] = query_params.get('limit')
        if limit is not None:
            try:
                limit = int(limit)
                if limit > self.max_limit:
                    query_params['limit'] = str(self.max_limit)
            except ValueError:
                return JSONResponse(status_code=400, content={'message': 'Invalid limit value'})

            # Construct the new query string
            new_query_string = urlencode(query_params)
            request.scope['query_string'] = new_query_string.encode('utf-8')

        response = await call_next(request)
        return response
