from aiogram import Router, Bot, types
from aiogram.utils.markdown import hlink, hbold

from src.api.dtos.user_dto import UserSettingsDTO
from src.bot.localization.languages import get_main_manu_lang

router = Router()


@router.message()
async def unknown_command(message: types.Message, settings: UserSettingsDTO):
    await message.answer(get_main_manu_lang(
        settings.selected_language or settings.language_code,
        'unsupported_command',
        message
    ))


async def send_notification(bot: Bot, owner_id: int, message: str, *, reply_markup=None):
    await bot.send_message(owner_id, message, reply_markup=reply_markup)


def new_offer(title, url, search_title):
    return f"Появился новый офер:\n{title}\n{hlink('Ссылка', url)}\nЗапрос: **{search_title}**"


def offer_title(title, url, search_title):
    return f"{title}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}"


def offer_description(description, url, search_title):
    return f"{description}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}"
