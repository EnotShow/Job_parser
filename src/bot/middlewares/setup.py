from aiogram import Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from src.bot.middlewares.CommandsMiddleware import CommandsMiddleware
from src.bot.middlewares.SettingsMiddleware import SettingsMiddleware


def register_middlewares(dp: Dispatcher):
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.message.middleware(SettingsMiddleware())
    dp.callback_query.middleware(SettingsMiddleware())

    dp.message.middleware(CommandsMiddleware())
