from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_manu_keyboard():
    buttons = {
        "searches": KeyboardButton(text="Поисковые запросы"),
        "profile": KeyboardButton(text="Профиль"),
        "statistics": KeyboardButton(text="Статистика"),
        "settings": KeyboardButton(text="⚙️")
    }

    main_manu_keyboard_builder = ReplyKeyboardBuilder()
    main_manu_keyboard_builder.add(
        buttons["searches"],
        buttons["profile"],
        buttons["statistics"],
        buttons["settings"])
    main_manu_keyboard_builder.adjust(3, 3)
    return main_manu_keyboard_builder.as_markup(resize_keyboard=True)
