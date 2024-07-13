import asyncio
from typing import List

import requests
from celery.exceptions import TaskError

from core.config.proj_settings import settings
from src.api.dtos.application_dto import ApplicationCreateDTO
from src.api.dtos.notification_dto import NotificationDTO
from src.api.dtos.search_dto import SearchFilterDTO
from src.bot.handlers.base import new_offer
from src.celery_worker.celery import celery_app
from src.parsers.helper import get_parser


@celery_app.task
def add_parsing_job(searches: [List[SearchFilterDTO], dict]):
    if isinstance(searches[0], dict):
        searches = [SearchFilterDTO(**search) for search in searches]
    asyncio.run(parsing_job(searches))


async def parsing_job(searches: [List[SearchFilterDTO], dict]):
    for search in searches:
        parser = await get_parser(search.url)
        result = await parser.parse_offers(search.url, search.owner_id)
        to_search = []
        for job in result:
            to_search.append(job.model_dump(exclude_none=True))

        find = requests.post(f"{settings.base_url}/application/find_multiple/", json=to_search).json()

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

        add_results = requests.post(f"{settings.base_url}/application/create_multiple/", json=to_add)
        if add_results.status_code != 200:
            raise TaskError(f"Failed to add jobs to database: {add_results.text}")

        send_notifications = requests.post(f"{settings.base_url}/notification/notify_multiple", json=to_add)
        if send_notifications.status_code != 200:
            raise TaskError(f"Failed to send notifications: {send_notifications.text}")

        for job in result:
            notification = NotificationDTO(
                owner_id=job.owner_id,
                message=new_offer(
                        job.title,
                        job.url,
                        search.title
                    ),
                social_network=job.social_network,
                social_network_id=job.social_network_id
            )

        return True
