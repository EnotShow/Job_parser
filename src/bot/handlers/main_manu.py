from aiogram import types, Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.payload import decode_payload
from dependency_injector.wiring import inject, Provide

from bot_create import bot
from src.api.containers.services_containers.application_service_container import ApplicationServiceContainer
from src.api.containers.services_containers.user_service_container import UserServiceContainer
from src.api.services.application_service import ApplicationService
from src.api.services.user_service import UserService
from src.bot.filters.text_filter import TextFilter
from src.bot.keyboards.main_menu_keyboard_buttons import get_main_manu_keyboard

main_manu_router = Router()


@main_manu_router.message(CommandStart())
@inject
async def main_manu(
        message: types.Message,
        command: CommandObject,
        user_service: UserService = Provide[UserServiceContainer.user_service]
):
    user = await user_service.get_user_by_telegram_id(message.from_user.id)
    if user is None:
        ref = None
        if command.args:
            payload = decode_payload(command.args)
            if payload.startswith("ref="):
                ref = payload.split("=")[1]
        await user_service.create_user_from_telegram(message, ref)
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=get_main_manu_keyboard())


@main_manu_router.message(Command('ref'))
@inject
async def get_ref_link(
        message: types.Message,
        user_service: UserService = Provide[UserServiceContainer.user_service],
):
    user = await user_service.get_user_by_telegram_id(message.from_user.id)
    ref_link = await create_start_link(bot, f"ref={user.id}", encode=True)
    await message.answer(ref_link)


@main_manu_router.message(TextFilter(text="Статистика"))
@inject
async def statistics(
        message: types.Message,
        application_service: ApplicationService = Provide[ApplicationServiceContainer.application_service]
):
    jobs_counter = await application_service.get_applications_by_telegram_id(telegram_id=message.from_user.id,
                                                                             count=True)
    await message.answer(
        f"Найденно для тебя работ: {jobs_counter}!",
        reply_markup=get_main_manu_keyboard()
    )
