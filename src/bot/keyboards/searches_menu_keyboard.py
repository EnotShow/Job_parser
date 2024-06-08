from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class SearchesCallbackData(CallbackData, prefix="searches"):
    callback: str


def get_searches_menu_keyboard():
    buttons = {
        "searches_list": InlineKeyboardButton(
            text="Список поисковых запросов", callback_data=SearchesCallbackData(callback="searches_list").pack()
        ),
        "add_search": InlineKeyboardButton(
            text="Добавить поисковый запрос", callback_data=SearchesCallbackData(callback="add_search").pack()
        ),
    }

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        buttons["searches_list"],
        buttons["add_search"],
    )
    keyboard_builder.adjust(1, 1)
    return keyboard_builder.as_markup(resize_keyboard=True)
