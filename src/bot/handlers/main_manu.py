from aiogram import types, Router
from aiogram.filters import CommandStart
from dependency_injector.wiring import inject, Provide

from src.api.containers.repositories_containers.user_repository_container import UserRepositoryContainer
from src.api.dtos.user_dto import UserDTO, UserCreateDTO
from src.api.repositories.user_repository import UserRepository
from src.bot.filters.text_filter import TextFilter
from src.bot.keyboards.main_menu_keyboard_buttons import get_main_manu_keyboard

main_manu_router = Router()


@inject
def get_users(user_repository: UserRepository = Provide[UserRepositoryContainer.user_repository]):
    return user_repository.get_all()


@main_manu_router.message(CommandStart())
@inject
async def main_manu(message: types.Message,
                    user_repository: UserRepository = Provide[UserRepositoryContainer.user_repository]):
    await message.answer("Firs")
    user_repository = UserRepository()
    users = await user_repository.get_all()
    print(users)
    # user = await user_repository.get_by_telegram_id(message.from_user.id)
    # if user is None:
    #     user_data = UserCreateDTO(
    #         telegram_id=message.from_user.id,
    #         language_code=message.from_user.language_code
    #     )
    #     await user_repository.create(user_data)
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=get_main_manu_keyboard())


@main_manu_router.message(TextFilter(text="Статистика"))
async def statistics(message: types.Message):
    jobs_counter = 10  # TODO: get from database
    await message.answer(
        f"Найденно для тебя работ: {jobs_counter}!",
        reply_markup=get_main_manu_keyboard()
    )
