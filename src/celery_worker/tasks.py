import asyncio
from typing import List

from celery.worker.state import requests

from parsers.helper import get_parser
from src.api.dtos.application_dto import ApplicationCreateDTO
from src.api.dtos.search_dto import SearchFilterDTO
from src.celery_worker.celery import celery_app


@celery_app.task
def add_parsing_job(searches: [List[SearchFilterDTO], dict]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parsing_job(searches))


async def parsing_job(searches: [List[SearchFilterDTO], dict]):
    for search in searches:
        parser = await get_parser(search.url)
        result = await parser.parse_offers(search.url, search.owner_id)
        to_search = []
        for job in result:
            to_search.append(job.model_dump(exclude_none=True))

        find = requests.post("http://127.0.0.1:8000/application/find_multiple/", json=to_search).json()

        existing_urls = [f['url'] for f in find]
        to_add = []
        for job in result[::-1]:
            if job.url not in existing_urls:
                model = ApplicationCreateDTO(
                    title=job.title,
                    description=job.description,
                    application_link=job.application_link,
                    url=job.url,
                    owner_id=job.owner_id,
                )
                to_add.append(model.model_dump())

        add_results = requests.post("http://127.0.0.1:8000/application/create_multiple/", json=to_add).json()

        return True
