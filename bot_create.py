from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from core.config.bot import settings_bot

WEBHOOK_PATH = f"/bot/{settings_bot.token}"
WEBHOOK_URL = settings_bot.webhook_url + WEBHOOK_PATH

storage = MemoryStorage()

bot = Bot(token=settings_bot.token, skip_updates=True)
dp = Dispatcher(storage=storage)


async def bot_update(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


async def set_webhook():
    await bot.set_webhook(url=WEBHOOK_URL, allowed_updates=['message', 'callback_query'], drop_pending_updates=True)


async def delete_webhook():
    await bot.delete_webhook()
