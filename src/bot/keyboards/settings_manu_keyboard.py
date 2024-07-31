import enum
from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.api.users.user_dto import UserSettingsDTO


class SettingsCallbackType(enum.StrEnum):
    LANGUAGE = "language"
    CHANGE_LANGUAGE = "change_language"
    PAUSING = "pausing"


class SettingsCallbackData(CallbackData, prefix="settings"):
    callback: SettingsCallbackType
    language_option: Optional[str] = None


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


def get_language_select_keyboard():
    languages = {"ru": "Русский", "pl": "Polski", "en": "English"}
    keyboard_builder = InlineKeyboardBuilder()
    for language in languages:
        keyboard_builder.add(
            InlineKeyboardButton(
                text=languages[language],
                callback_data=SettingsCallbackData(
                    callback=SettingsCallbackType.CHANGE_LANGUAGE, language_option=language
                ).pack()
            )
        )
    keyboard_builder.adjust(3, 3)
    return keyboard_builder.as_markup(resize_keyboard=True)
