from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_manu_keyboard(lang: str = None, return_buttons_list: bool = False, button: str = None):
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
    if return_buttons_list:
        button_list = []
        for lang_code, lang_buttons in translate.items():
            if button in lang_buttons:
                button_list.append(lang_buttons[button].text)
        return button_list

    main_manu_keyboard_builder = ReplyKeyboardBuilder()
    main_manu_keyboard_builder.add(
        translate[lang]["searches"],
        translate[lang]["profile"],
        translate[lang]["statistics"],
        translate[lang]["settings"])
    main_manu_keyboard_builder.adjust(3, 3)
    return main_manu_keyboard_builder.as_markup(resize_keyboard=True)
