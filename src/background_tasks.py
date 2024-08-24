import asyncio

from dependency_injector.wiring import inject, Provide

from src.api.searches.containers.search_service_container import SearchServiceContainer
from src.api.searches.searchings_service import SearchService
from src.celery_worker.helpers import convert_to_celery_primitive
from src.celery_worker.tasks.link_parser import add_parsing_job


@inject
async def processing(
        searching_service: SearchService = Provide[SearchServiceContainer.search_service],
):
    while True:
        try:
            searches = await searching_service.get_all_searches()
            searches = convert_to_celery_primitive(searches.items)
            for i in range(0, len(searches), 100):
                batch = searches[i:i + 100]
                add_parsing_job.apply_async((batch,))
        except Exception as e:
            print(e)
        await asyncio.sleep(1)
