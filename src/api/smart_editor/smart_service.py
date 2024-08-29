from src.api.smart_editor.errors import CacheBrokerConnectionError, ProcesAlreadyRunningError
from src.api.smart_editor.smart_dto import SmartEditorParamsDTO, SmartProcessHashDTO
from src.api.smart_editor.smart_repository import SmartHashRepository
from src.celery_worker.tasks.smart_link_generator import add_create_smart_link_job


class SmartService:
    _repository = SmartHashRepository()

    async def smart_links_create(self, params_dto: SmartEditorParamsDTO):
        try:
            hash_dto = SmartProcessHashDTO(
                owner_id=params_dto.owner_id,
            )
            find = await self._repository.find(hash_dto)
            if not find:
                add_create_smart_link_job.delay(params_dto)
            else:
                raise ProcesAlreadyRunningError
            await self._repository.create(hash_dto, expire=30 * 60)
            return True
        except ProcesAlreadyRunningError as e:
            raise e
        except Exception as e:
            raise CacheBrokerConnectionError(e)

    async def smart_links_process_delete_hash(self, params_dto: SmartEditorParamsDTO):
        try:
            hash_dto = SmartProcessHashDTO(
                owner_id=params_dto.owner_id,
            )
            await self._repository.delete(hash_dto.pk)
            return True
        except Exception as e:
            raise CacheBrokerConnectionError(e)
