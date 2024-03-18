from aiogram import Dispatcher

from src.handlers import router


def register_bot_routes(dp: Dispatcher):
    dp.include_router(router)
