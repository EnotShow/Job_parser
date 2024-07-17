from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_manu_keyboard(lang: str):
    translate = {
        "ru": {
            "searches": KeyboardButton(text="Поисковые запросы"),
            "profile": KeyboardButton(text="Профиль"),
            "statistics": KeyboardButton(text="Статистика"),
            "settings": KeyboardButton(text="⚙️")
        },
        "pl": {
            "searches": KeyboardButton(text="Wyszukiwarki"),
            "profile": KeyboardButton(text="Profil"),
            "statistics": KeyboardButton(text="Statystyki"),
            "settings": KeyboardButton(text="⚙️")
        },
        "en": {
            "searches": KeyboardButton(text="Searches"),
            "profile": KeyboardButton(text="Profile"),
            "statistics": KeyboardButton(text="Statistics"),
            "settings": KeyboardButton(text="⚙️")
        }
    }

    main_manu_keyboard_builder = ReplyKeyboardBuilder()
    main_manu_keyboard_builder.add(
        translate[lang]["searches"],
        translate[lang]["profile"],
        translate[lang]["statistics"],
        translate[lang]["settings"])
    main_manu_keyboard_builder.adjust(3, 3)
    return main_manu_keyboard_builder.as_markup(resize_keyboard=True)
