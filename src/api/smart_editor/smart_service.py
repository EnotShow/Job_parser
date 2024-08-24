from src.api.smart_editor.smart_dto import SmartEditorParamsDTO
from src.celery_worker.tasks.smart_link_generator import add_create_smart_link_job


class SmartService:

    async def smart_links_create(self, params_dto: SmartEditorParamsDTO):
        add_create_smart_link_job.delay(params_dto)
        return True
