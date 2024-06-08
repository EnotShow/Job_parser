from aiogram import types, Router
from aiogram.filters import CommandStart
from dependency_injector.wiring import inject, Provide

from src.api.containers.repositories_containers.user_repository_container import UserRepositoryContainer
from src.api.containers.services_containers.user_service_container import UserServiceContainer
from src.api.dtos.user_dto import UserDTO, UserCreateDTO
from src.api.repositories.user_repository import UserRepository
from src.api.services.user_service import UserService
from src.bot.filters.text_filter import TextFilter
from src.bot.keyboards.main_menu_keyboard_buttons import get_main_manu_keyboard

main_manu_router = Router()


@main_manu_router.message(CommandStart())
@inject
async def main_manu(message: types.Message, user_service: UserService = Provide[UserServiceContainer.user_service]):
    user = await user_service.get_user_by_telegram_id(message.from_user.id)
    if user is None:
        await user_service.create_user_from_telegram(message)
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=get_main_manu_keyboard())


@main_manu_router.message(TextFilter(text="Статистика"))
async def statistics(message: types.Message):
    jobs_counter = 10  # TODO: get from database
    await message.answer(
        f"Найденно для тебя работ: {jobs_counter}!",
        reply_markup=get_main_manu_keyboard()
    )
