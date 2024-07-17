from aiogram.types import InlineKeyboardButton

from src.bot.filters.callbackquery_filter import ReplyType, ReplyCallback


class ReplyCallbackButtons:

    @staticmethod
    def button_title(application_id: int, search_title: str, lang: str):
        translate = {
            "ru": "Заголовок",
            "pl": "Tytuł",
            "en": "Title"
        }
        return InlineKeyboardButton(text=translate[lang], callback_data=ReplyCallback(
            type=ReplyType.TITLE,
            application_id=application_id,
            search_title=search_title
        ).pack())

    @staticmethod
    def button_description(application_id: int, search_title: str, lang: str):
        translate = {
            "ru": "Описание",
            "pl": "Tresc",
            "en": "Description"
        }
        return InlineKeyboardButton(text=translate[lang], callback_data=ReplyCallback(
            type=ReplyType.DESCRIPTION,
            application_id=application_id,
            search_title=search_title
        ).pack())

    @staticmethod
    def button_apply(application_id, search_title):
        translate = {
            "ru": "Подать заявку",
            "pl": "Zatwierdź zapytanie",
            "en": "Apply"
        }
        return InlineKeyboardButton(text=translate["en"], callback_data=ReplyCallback(
            type=ReplyType.APPLY,
            application_id=application_id,
            search_title=search_title
        ).pack())
