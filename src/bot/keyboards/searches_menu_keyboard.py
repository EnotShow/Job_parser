from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class SearchesCallbackData(CallbackData, prefix="searches"):
    callback: str
    search_id: Optional[int] = None


def get_searches_menu_keyboard(
        lang: str = None, return_buttons_list: bool = False, button: str = None) -> [InlineKeyboardMarkup, str]:
    translate = {
        "ru": {
            "searches_list": InlineKeyboardButton(
                text="Список поисковых запросов", callback_data=SearchesCallbackData(callback="searches_list").pack()
            ),
            "add_search": InlineKeyboardButton(
                text="Добавить поисковый запрос", callback_data=SearchesCallbackData(callback="add_search").pack()
            ),
        },
        "pl": {
            "searches_list": InlineKeyboardButton(
                text="Lista wyszukiwarków", callback_data=SearchesCallbackData(callback="searches_list").pack()
            ),
            "add_search": InlineKeyboardButton(
                text="Dodaj wyszukiwarkę", callback_data=SearchesCallbackData(callback="add_search").pack()
            ),
        },
        "en": {
            "searches_list": InlineKeyboardButton(
                text="Searches list", callback_data=SearchesCallbackData(callback="searches_list").pack()
            ),
            "add_search": InlineKeyboardButton(
                text="Add search", callback_data=SearchesCallbackData(callback="add_search").pack()
            ),
        },
    }
    if return_buttons_list:
        button_list = []
        for lang_code, lang_buttons in translate.items():
            if button in lang_buttons:
                button_list.append(lang_buttons[button].text)
        return button_list

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        translate[lang]["searches_list"],
        translate[lang]["add_search"],
    )
    keyboard_builder.adjust(1, 1)
    return keyboard_builder.as_markup(resize_keyboard=True)


def get_searches_list_menu_keyboard(
        search_id: int = None,
        lang: str = None,
        return_buttons_list: bool = False,
        button: str = None
) -> [InlineKeyboardMarkup, str]:
    translate = {
        "ru": {
            "search_update": InlineKeyboardButton(
                text="Изменить поисковой запрос", callback_data=SearchesCallbackData(
                    callback="change_search", search_id=search_id).pack()
            ),
            "delete_search": InlineKeyboardButton(
                text="🗑", callback_data=SearchesCallbackData(
                    callback="delete_search", search_id=search_id).pack()
            ),
        },
        "pl": {
            "search_update": InlineKeyboardButton(
                text="Zaktualizuj wyszukiwarkę", callback_data=SearchesCallbackData(
                    callback="change_search", search_id=search_id).pack()
            ),
            "delete_search": InlineKeyboardButton(
                text="🗑", callback_data=SearchesCallbackData(
                    callback="delete_search", search_id=search_id).pack()
            ),
        },
        "en": {
            "search_update": InlineKeyboardButton(
                text="Update search", callback_data=SearchesCallbackData(
                    callback="change_search", search_id=search_id).pack()
            ),
            "delete_search": InlineKeyboardButton(
                text="🗑", callback_data=SearchesCallbackData(
                    callback="delete_search", search_id=search_id).pack()
            ),
        },
    }
    if return_buttons_list:
        button_list = []
        for lang_code, lang_buttons in translate.items():
            if button in lang_buttons:
                button_list.append(lang_buttons[button].text)
        return button_list

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(*translate[lang].values())
    keyboard_builder.adjust(2, 2)
    return keyboard_builder.as_markup(resize_keyboard=True)
