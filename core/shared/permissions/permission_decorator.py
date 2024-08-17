from functools import wraps
from typing import List, TypeVar, Callable

from starlette.responses import JSONResponse

from core.shared.permissions.BasePermission import BasePermission

T = TypeVar('T', bound=BasePermission)


def permission_required(permissions: List[T]) -> Callable:

    def decorator(f: Callable):

        @wraps(f)
        async def wrapper(*args, **kwargs):
            for permission in permissions:
                if await permission.is_permitted(*args, **kwargs):
                    return await f(*args, **kwargs)
            return JSONResponse(content={"detail": "Permission denied"}, status_code=403)

        return wrapper

    return decorator
