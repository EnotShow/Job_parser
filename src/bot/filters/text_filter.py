from aiogram import Bot, types
from aiogram.filters import Filter


class TextFilter(Filter):
    def __init__(self, text_list: str):
        self.text_list = text_list

    async def __call__(self, message: types.Message, bot: Bot):
        if message.text in self.text_list:
            return True
        return False
