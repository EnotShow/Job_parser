from aiogram import Dispatcher

from src.bot.handlers.base import router as base_router
from src.bot.handlers.reply import router as reply_router


def register_bot_routes(dp: Dispatcher):
    dp.include_router(base_router)
    dp.include_router(reply_router)
