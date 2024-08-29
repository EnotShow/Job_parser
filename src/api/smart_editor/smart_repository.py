from typing import List

from core.shared.base_repository import CacheRepository
from src.api.smart_editor.smart_cache_models import SmartProcessHash
from src.api.smart_editor.smart_dto import SmartProcessHashDTO


class SmartHashRepository(CacheRepository):
    model = SmartProcessHash

    async def create(self, dto: SmartProcessHashDTO, expire: int) -> SmartProcessHashDTO:
        instance = self.model(user_id=dto.user_id)
        await instance.expire(expire)
        await instance.save()
        dto.pk = instance.pk
        return dto

    async def get(self, pk) -> SmartProcessHashDTO | None:
        instance = await self.model.get(pk)
        if instance is None:
            return None
        return SmartProcessHashDTO(pk=instance.pk, user_id=instance.user_id)

    async def find_single(self, dto: SmartProcessHashDTO) -> SmartProcessHashDTO | None:
        instance = await self.model.find(
            self.model.hash == dto.hash, self.model.user_id == dto.user_id
        ).first()
        if instance is None:
            return None
        return SmartProcessHashDTO(pk=instance.pk, user_id=instance.user_id)

    async def find(self, dto: SmartProcessHashDTO) -> List[SmartProcessHashDTO] | None:
        instances = await self.model.find(
            self.model.hash == dto.hash, self.model.user_id == dto.user_id
        ).all()
        if instances is None:
            return None
        return [SmartProcessHashDTO(pk=instance.pk, user_id=instance.user_id) for instance in instances]

    async def delete(self, pk: str) -> bool:
        await self.model.delete(self.model.pk == pk)
        return True




