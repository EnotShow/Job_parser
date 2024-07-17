import asyncio
from typing import TypeVar, List

from dependency_injector.wiring import inject, Provide

from core.shared.base_dto import BaseDTO
from src.api.containers.services_containers.search_service_container import SearchServiceContainer
from src.api.services.searchings_service import SearchService
from src.celery_worker.tasks import add_parsing_job

T = TypeVar("T", bound=BaseDTO)


@inject
async def processing(
        searching_service: SearchService = Provide[SearchServiceContainer.search_service],
):
    while True:
        def to_celery_primitive(objects: List[T]) -> List[T]:
            return [obj.model_dump() for obj in objects]

        print('Processing...')
        searches = await searching_service.get_all_searches()
        searches = to_celery_primitive(searches)
        for i in range(0, len(searches), 100):
            batch = searches[i:i + 100]
            add_parsing_job.apply_async((batch,))
        await asyncio.sleep(60 * 1)

if __name__ == '__main__':
    processing()
