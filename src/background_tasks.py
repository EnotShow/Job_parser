import asyncio

from aiogram.types import InlineKeyboardMarkup

from bot_create import bot
from core.config.bot import settings_bot
from core.db.db_helper import db_helper
from parsers.helper import get_parser
from src.bot.handlers.base import send_notification, new_offer
from src.bot.keyboards.reply_keyboard_buttons import ReplyCallbackButtons
from src.api.repositories.application_repository import ApplicationRepository
from src.api.repositories.searchings_repository import SearchRepository


async def processing():
    while True:
        async with db_helper.get_db_session() as session:
            Searching_repository = SearchRepository(session)
            searches = await Searching_repository.get_all()
            for search in searches:
                parser = await get_parser(search.url)
                result = await parser.parse_offers(search.url)
                application_repository = ApplicationRepository(session)
                application_to_create = []
                for job in result:
                    find = await application_repository.get_by_url(job.url)
                    if not find:
                        application_to_create.append(job)
                        message = new_offer(
                            job.title,
                            job.url,
                            search.title
                        )
                        application = await application_repository.create(job)
                        reply_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[
                            ReplyCallbackButtons.button_description(
                                application.id, search.title),
                            ReplyCallbackButtons.button_apply(
                                application.id, search.title)
                        ]])
                        await send_notification(bot, settings_bot.owners, message, reply_markup=reply_keyboard)
                # await application_repository.create_multiple(application_to_create)
            await asyncio.sleep(60 * 10)
