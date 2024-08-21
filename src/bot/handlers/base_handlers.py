from aiogram import Router, Bot, types
from aiogram.utils.markdown import hlink, hbold

from src.api.users.user_dto import UserSettingsDTO
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


def new_offer(title, url, search_title, lang):
    translate = {
        'ru': f"Появился новый офер:\n{title}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}",
        'pl': f"Został dodany nowy ofer:\n{title}\n{hlink('Ссылка', url)}\nZapytanie: {hbold(search_title)}",
        'en': f"New offer appeared:\n{title}\n{hlink('Link', url)}\nSearch: {hbold(search_title)}",
    }
    return translate[lang]


def offer_title(title, url, search_title, lang):
    translate = {
        'ru': f"{title}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}",
        'pl': f"{title}\n{hlink('Plik', url)}\nZapyt: {hbold(search_title)}",
        'en': f"{title}\n{hlink('Link', url)}\nSearch: {hbold(search_title)}",
    }
    return translate[lang]


def offer_description(description, url, search_title, lang):
    translate = {
        'ru': f"{description}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}",
        'pl': f"{description}\n{hlink('Plik', url)}\nZapyt: {hbold(search_title)}",
        'en': f"{description}\n{hlink('Link', url)}\nSearch: {hbold(search_title)}",
    }
    return translate[lang]
