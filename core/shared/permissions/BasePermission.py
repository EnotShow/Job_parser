from starlette.requests import Request


class BasePermission:

    @staticmethod
    async def is_permitted(request: Request, *args, **kwargs):
        return True
