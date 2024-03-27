from aiogram.types import InlineKeyboardButton

from src.bot.filters.callbackquery_filter import ReplyType, ReplyCallback


class ReplyCallbackButtons:

    @staticmethod
    def button_title(application_id, search_title):
        return InlineKeyboardButton(text="Заголовок", callback_data=ReplyCallback(
            type=ReplyType.TITLE,
            application_id=application_id,
            search_title=search_title
        ).pack())

    @staticmethod
    def button_description(application_id, search_title):
        return InlineKeyboardButton(text="Описание", callback_data=ReplyCallback(
            type=ReplyType.DESCRIPTION,
            application_id=application_id,
            search_title=search_title
        ).pack())

    @staticmethod
    def button_apply(application_id, search_title):
        return InlineKeyboardButton(text="Подать заявку", callback_data=ReplyCallback(
            type=ReplyType.APPLY,
            application_id=application_id,
            search_title=search_title
        ).pack())
