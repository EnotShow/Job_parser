from src.api.auth.services.jwt_service import jwt_service


async def decode_token(token: str):
    return await jwt_service.decode_token(token)
