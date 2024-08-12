import asyncio
from typing import List

from celery.exceptions import TaskError

from core.config.proj_settings import settings
from core.shared.enums import SocialNetworkEnum
from src.api.applications.application_dto import ApplicationCreateDTO, ApplicationFullDTO
from src.api.messangers.dtos.notification_dto import NotificationDTO
from src.api.searches.search_dto import SearchFilterDTO
from src.bot.handlers.base_handlers import new_offer
from src.celery_worker.celery import celery_app
from src.client.client import JobParserClient
from src.parsers.helper import get_parser


@celery_app.task(bind=True, autoretry_for=(TaskError,), retry_kwargs={'max_retries': 2})
def add_parsing_job(searches: [List[SearchFilterDTO], dict]):
    if isinstance(searches[0], dict):
        searches = [SearchFilterDTO(**search) for search in searches]
    asyncio.run(parsing_job(searches))


async def parsing_job(searches: [List[SearchFilterDTO], dict]):
    client = JobParserClient()
    await client.auth_as_service(settings.service_api_key)

    for search in searches:
        parser = await get_parser(search.url)
        result = await parser.parse_offers(search.url, search.owner_id)
        to_search = []
        for job in result:
            to_search.append(job.model_dump(exclude_none=True))

        await client.applications.service.find_multiple(to_search)
        try:
            find = await client.applications.service.get_applications_if_exists(to_search)
        except Exception:
            raise TaskError(f"Failed to find jobs in database")

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

        try:
            add_results = await client.applications.service.create_multiple_applications(to_add)
        except Exception:
            raise TaskError(f"Failed to add jobs to database")
        result = [ApplicationFullDTO(**res) for res in add_results.json()]
        notifications = []

        for job in result:
            notification = NotificationDTO(
                owner_id=job.owner_id,
                message=new_offer(
                        job.title,
                        job.short_url,
                        search.title,
                        job.owner.selected_language
                    ),
                social_network=SocialNetworkEnum.telegram,
                social_network_id=job.owner.telegram_id
            )
            notifications.append(notification.model_dump())
        try:
            await client.notifications.send_multiple_notifications(notifications)
        except Exception:
            raise TaskError(f"Failed to send notifications")

        return True
