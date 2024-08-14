from typing import List, Optional

from core.shared.base_repository import CacheRepository
from src.api.auth.auth_cache_models import AuthHash
from src.api.auth.auth_dto import AuthHashDTO


class AuthHashRepository(CacheRepository):
    model = AuthHash

    async def create(self, dto: AuthHashDTO, expire: Optional[int] = None) -> AuthHashDTO:
        instance = self.model(user_id=dto.user_id)
        await instance.expire(expire)
        await instance.save()
        dto.pk = instance.pk
        return dto

    async def get(self, pk) -> AuthHashDTO | None:
        instance = await self.model.get(self.model.pk == pk)
        if instance is None:
            return None
        return AuthHashDTO(pk=instance.pk, user_id=instance.user_id)

    async def find_single(self, dto: AuthHashDTO) -> AuthHashDTO | None:
        instance = await self.model.find(
            self.model.hash == dto.hash, self.model.user_id == dto.user_id
        ).first()
        if instance is None:
            return None
        return AuthHashDTO(pk=instance.pk, user_id=instance.user_id)

    async def find(self, dto: AuthHashDTO) -> List[AuthHashDTO] | None:
        instances = await self.model.find(
            self.model.hash == dto.hash, self.model.user_id == dto.user_id
        ).all()
        if instances is None:
            return None
        return [AuthHashDTO(pk=instance.pk, user_id=instance.user_id) for instance in instances]

    async def delete(self, pk: str) -> bool:
        await self.model.delete(self.model.pk == pk)
        return True




