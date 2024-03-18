from aiogram import types, Router, Bot
from aiogram.filters import Command
from aiogram.utils.markdown import hlink, hbold

router = Router()


def new_offer(title, url, search_title):
    return f"Появился новый офер:\n{title}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}"


async def send_notification(bot: Bot, owner_id: int, message: str):
    await bot.send_message(owner_id, message)
