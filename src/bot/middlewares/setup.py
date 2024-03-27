from aiogram import Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from core.config.bot import settings_bot


def register_middlewares(dp: Dispatcher):
    dp.callback_query.middleware(CallbackAnswerMiddleware())
