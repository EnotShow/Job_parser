from aiogram import types, Router
from aiogram.filters import CommandStart
from dependency_injector.wiring import inject

from src.api.dependencies.IUserService import IUserService
from src.bot.filters.text_filter import TextFilter
from src.bot.keyboards.main_menu_keyboard_buttons import get_main_manu_keyboard

main_manu_router = Router()


@inject
@main_manu_router.message(CommandStart())
async def main_manu(message: types.Message):
    print('work')
    user_service = IUserService
    user = await user_service.get_user(dto=)
    print(user)
    if not user:
        await user_service.add_user(message.from_user)
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=get_main_manu_keyboard())


@main_manu_router.message(TextFilter(text="Статистика"))
async def statistics(message: types.Message):
    jobs_counter = 10  # TODO: get from database
    await message.answer(
        f"Найденно для тебя работ: {jobs_counter}!",
        reply_markup=get_main_manu_keyboard()
    )
