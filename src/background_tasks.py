import asyncio

from aiogram.types import InlineKeyboardMarkup
from dependency_injector.wiring import inject, Provide

from bot_create import bot
from parsers.helper import get_parser
from src.api.containers.services_containers.search_service_container import SearchServiceContainer
from src.api.services.application_service import ApplicationService
from src.api.services.searchings_service import SearchService
from src.bot.handlers.base import send_notification, new_offer
from src.bot.keyboards.reply_keyboard_buttons import ReplyCallbackButtons


@inject
async def processing(
        searching_service: SearchService = Provide[SearchServiceContainer.searching_service],
        application_service: ApplicationService = Provide[SearchServiceContainer.application_service]
):
    while True:
        searches = await searching_service.get_all_searches()
        for search in searches:
            parser = await get_parser(search.url)
            result = await parser.parse_offers(search.url)
            application_to_create = []
            for job in result:
                find = await application_service.get_application_by_url(job.url)
                if not find:
                    application_to_create.append(job)
                    message = new_offer(
                        job.title,
                        job.url,
                        search.title
                    )
                    application = await application_service.create_application(job)
                    reply_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[
                        ReplyCallbackButtons.button_description(
                            application.id, search.title),
                        ReplyCallbackButtons.button_apply(
                            application.id, search.title)
                    ]])
                    await send_notification(bot, search.owner_id, message, reply_markup=reply_keyboard)
            await asyncio.sleep(60 * 10)
