from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hlink, hbold

router = Router()


async def send_notification(bot: Bot, owner_id: int, message: str, *, reply_markup=None):
    await bot.send_message(owner_id, message, reply_markup=reply_markup)

def new_offer(title, url, search_title):
    return f"Появился новый офер:\n{title}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}"


def offer_title(title, url, search_title):
    return f"{title}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}"


def offer_description(description, url, search_title):
    return f"{description}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}"
