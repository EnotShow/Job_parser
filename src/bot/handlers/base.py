from aiogram import Router, Bot
from aiogram.filters import CommandStart

router = Router()


async def send_notification(bot: Bot, owner_id: int, message: str, *, reply_markup=None):
    await bot.send_message(owner_id, message, reply_markup=reply_markup)


@router.message(CommandStart())
async def start(message):
    await message.answer(f"Hello, {message.from_user.full_name}!")