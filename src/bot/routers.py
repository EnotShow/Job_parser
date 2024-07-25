from aiogram import Dispatcher

from src.bot.handlers.base_handlers import router as base_router
from src.bot.handlers.main_manu_handlers import main_manu_router
from src.bot.handlers.reply_handlers import router as reply_router
from src.bot.handlers.searches_handlers import searches_router
from src.bot.handlers.settings_handlers import settings_router


def register_bot_routes(dp: Dispatcher):
    dp.include_router(reply_router)
    dp.include_router(main_manu_router)
    dp.include_router(searches_router)
    dp.include_router(settings_router)
    dp.include_router(base_router)

