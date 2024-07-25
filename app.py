import asyncio
import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware

from bot_create import dp, WEBHOOK_PATH, bot_update, set_webhook, delete_webhook
from core.config.proj_settings import settings, development_settings
from core.db.db_helper import db_helper
from core.scripts.command_list import execute_command
from src.admin.admin_routers import add_admin_views
from src.api.containers.containers_builder import build_containers
from src.api.routes import get_apps_router
from src.background_tasks import processing
from src.bot.middlewares.setup import register_middlewares
from src.bot.routers import register_bot_routes

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Bot is starting...')
    if development_settings.background_tasks:
        print('Background tasks are running...')
        asyncio.create_task(processing())
    await set_webhook()
    print('Webhook is set...')
    print('Bot ready for work!')

    yield
    await delete_webhook()
    print('Bot is stopping...')


def get_application() -> FastAPI:
    build_containers()

    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version=settings.version,
        lifespan=lifespan
    )
    application.include_router(get_apps_router())

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()


@app.post(WEBHOOK_PATH, include_in_schema=False)
async def bot_webhook(update: dict):
    await bot_update(update)


# Register admin
admin = Admin(
    app,
    engine=db_helper.engine,
    session_maker=db_helper.session_factory,
    # authentication_backend=authentication_backend,
)

add_admin_views(admin)

# Register middlewares
register_middlewares(dp)

# Register routes
register_bot_routes(dp)

if __name__ == "__main__":
    execute_command(sys.argv)

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
