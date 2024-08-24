import asyncio

from celery.exceptions import TaskError

from core.config.proj_settings import development_settings
from src.api.searches.search_dto import SearchCreateDTO
from src.api.smart_editor.smart_dto import SmartEditorParamsDTO
from src.celery_worker.celery import celery_app
from src.client.client import JobParserClient
from src.parsers.helpers.get_link_generator import get_link_generator


@celery_app.task(bind=True, autoretry_for=(TaskError,), retry_kwargs={'max_retries': 2})
def add_create_smart_link_job(smart_dto: [SmartEditorParamsDTO, dict]):
    if isinstance(smart_dto, dict):
        smart_dto = SmartEditorParamsDTO(**smart_dto)
    asyncio.run(create_smart_links(smart_dto))


async def create_smart_links(smart_dto: SmartEditorParamsDTO):
    client = JobParserClient()
    await client.auth_as_service(development_settings.service_api_token)
    links_limit = smart_dto.links_limit

    searches_to_create = []

    for service in smart_dto.services:
        if links_limit:
            link_generator = await get_link_generator(service)
            link = await link_generator.generate_link(smart_dto)
            searches_to_create.append(
                SearchCreateDTO(title=smart_dto.kwords, url=link, owner_id=smart_dto.owner_id)
            )
        else:
            break

    await client.searches.service.create_searches(searches_to_create)
