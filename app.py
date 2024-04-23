import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
import flet.fastapi as flet_fastapi
from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware

from bot_create import dp, WEBHOOK_PATH, bot_update, set_webhook, delete_webhook
from core.config.proj_settings import settings
from core.db.db_helper import db_helper
from core.scripts.command_list import execute_command
from src.admin.admin_routers import add_admin_views
from src.admin.auth.admin import authentication_backend
from src.background_tasks import processing
from src.bot.middlewares.setup import register_middlewares
from src.routers import register_bot_routes
from src.web.routes import add_web_routes

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Bot is starting...')
    # asyncio.create_task(processing())
    await flet_fastapi.app_manager.start()
    # await set_webhook()

    yield
    # await delete_webhook()
    await flet_fastapi.app_manager.shutdown()
    print('Bot is stopping...')


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version=settings.version,
        lifespan=lifespan
    )
    add_web_routes(application)

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
admin = Admin(
    app,
    engine=db_helper.engine,
    session_maker=db_helper.session_factory,
    authentication_backend=authentication_backend,
    base_url='/admin'
)

add_admin_views(admin)

# Register middlewares
register_middlewares(dp)

# Register routes
register_bot_routes(dp)


@app.post(WEBHOOK_PATH, include_in_schema=False)
async def bot_webhook(update: dict):
    await bot_update(update)


if __name__ == "__main__":
    execute_command(sys.argv)

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
