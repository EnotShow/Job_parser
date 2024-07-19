from aiogram import Dispatcher

from src.bot.handlers.base import router as base_router
from src.bot.handlers.main_manu import main_manu_router
from src.bot.handlers.reply import router as reply_router
from src.bot.handlers.searches import searches_router


def register_bot_routes(dp: Dispatcher):
    dp.include_router(reply_router)
    dp.include_router(main_manu_router)
    dp.include_router(searches_router)
    dp.include_router(base_router)
