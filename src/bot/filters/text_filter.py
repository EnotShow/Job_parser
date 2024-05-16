from aiogram import Bot, types
from aiogram.filters import Filter


class TextFilter(Filter):
    def __init__(self, text: str):
        self.text = text

    async def __call__(self, message: types.Message, bot: Bot):
        if message.text == self.text:
            return True
        return False
