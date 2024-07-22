import enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.api.dtos.user_dto import UserSettingsDTO


class SettingsCallbackType(enum.StrEnum):
    LANGUAGE = "language"
    PAUSING = "pausing"


class SettingsCallbackData(CallbackData, prefix="settings"):
    callback: SettingsCallbackType


def get_settings_menu_keyboard(
        settings: UserSettingsDTO = None,
        return_buttons_list: bool = False,
        button: str = None
) -> [InlineKeyboardMarkup, str]:
    translate = {
        "ru": {
            "language": InlineKeyboardButton(
                text=f"Ваш текущий язык: Русский",
                callback_data=SettingsCallbackData(callback=SettingsCallbackType.LANGUAGE).pack()
            ),
            "pausing": InlineKeyboardButton(
                text=f"Поиск вакансий: {"Включен" if not settings.paused else "Выключен"}",
                callback_data=SettingsCallbackData(callback=SettingsCallbackType.PAUSING).pack()
            ),
        },
        "pl": {
            "language": InlineKeyboardButton(
                text=f"Twoj aktualny jezyk: Polski",
                callback_data=SettingsCallbackData(callback=SettingsCallbackType.LANGUAGE).pack()
            ),
            "pausing": InlineKeyboardButton(
                text=f"Wyszukiwanie wakacji: {"Wlaczone" if not settings.paused else "Wylaczone"}",
                callback_data=SettingsCallbackData(callback=SettingsCallbackType.PAUSING).pack()
            ),
        },
        "en": {
            "language": InlineKeyboardButton(
                text=f"Your current language: English",
                callback_data=SettingsCallbackData(callback=SettingsCallbackType.LANGUAGE).pack()
            ),
            "pausing": InlineKeyboardButton(
                text=f"Job search: {"Enabled" if not settings.paused else "Disabled"}",
                callback_data=SettingsCallbackData(callback=SettingsCallbackType.PAUSING).pack()
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
        translate[settings.selected_language]["language"],
        translate[settings.selected_language]["pausing"],
    )
    keyboard_builder.adjust(1, 1)
    return keyboard_builder.as_markup(resize_keyboard=True)
