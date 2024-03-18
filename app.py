import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware

from core.config.bot import settings_bot
from core.config.proj_settings import settings
from core.db.db_helper import db_helper
from parsers.helper import get_parser
from src.admin_views import add_admin_views
from src.handlers import new_offer, send_notification
from src.middlewares.owner import OwnersMiddleware
from src.repositories.application_repository import ApplicationRepository
from src.repositories.searchings_repository import SearchingRepository
from src.routers import register_bot_routes

logger = logging.getLogger(__name__)

WEBHOOK_PATH = f"/bot/{settings_bot.token}"
WEBHOOK_URL = settings_bot.webhook_url + WEBHOOK_PATH

storage = MemoryStorage()

bot = Bot(token=settings_bot.token, parse_mode="HTML")
dp = Dispatcher(storage=storage)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(processing())
    await bot.set_webhook(url=WEBHOOK_URL)

    yield
    await bot.delete_webhook()


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version=settings.version,
        lifespan=lifespan
    )
    # application.include_router(get_apps_router())

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()

# Register admin
admin = Admin(app, engine=db_helper.engine, session_maker=db_helper.session_factory)
add_admin_views(admin)

# Register middlewares
dp.update.middleware(OwnersMiddleware([int(settings_bot.owners)]))

# Register routes
register_bot_routes(dp)


@app.post(WEBHOOK_PATH, include_in_schema=False)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


async def processing():
    while True:
        async with db_helper.get_db_session() as session:
            Searching_repository = SearchingRepository(session)
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
                        message = new_offer(job.title, job.url, search.title)
                        await send_notification(bot, settings_bot.owners, message)
                await application_repository.create_multiple(application_to_create)
            await asyncio.sleep(60*10)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
