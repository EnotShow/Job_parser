import asyncio
from typing import List

from celery.exceptions import TaskError

from core.config.proj_settings import development_settings
from core.shared.enums import SocialNetworkEnum
from core.shared.errors import NoRowsFoundError
from src.api.applications.application_dto import ApplicationCreateDTO, ApplicationFilterDTO
from src.api.messangers.dtos.notification_dto import MessangerNotificationDTO
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
    await client.auth_as_service(development_settings.service_api_token)

    for search in searches:
        parser = await get_parser(search.url)
        result = await parser.parse_offers(search.url, search.owner_id)
        to_search = []
        for job in result:
            to_search.append(ApplicationFilterDTO(**job.model_dump(exclude_none=True)))

        try:
            find = await client.applications.service.get_applications_if_exists(to_search)
        except NoRowsFoundError:
            pass
        except Exception as e:
            raise TaskError(f"Unexpected error when searching for jobs; {e}")

        existing_urls = [f.url for f in find]
        to_add = []
        for job in result[::-1]:
            if job.url not in existing_urls:
                model = ApplicationCreateDTO(
                    title=job.title,
                    description=job.description,
                    url=job.url,
                    owner_id=job.owner_id,
                )
                to_add.append(model)

        try:
            creates = await client.applications.service.create_multiple_applications(to_add)
        except Exception:
            raise TaskError(f"Failed to add jobs to database")
        notifications = []

        for job in creates:
            notification = MessangerNotificationDTO(
                owner_id=job.owner_id,
                message=new_offer(
                        job.title,
                        job.short_url,
                        search.title,
                        job.owner.selected_language
                    ),
                social_network=SocialNetworkEnum.telegram,
                social_network_id=job.owner.telegram_id,
                search_title=search.title,
                application_id=job.id,
                language=job.owner.selected_language
            )
            notifications.append(notification)
        try:
            await client.notifications.send_multiple_notifications(notifications)
        except Exception as e:
            raise TaskError(f"Failed to send notifications")

        return True
