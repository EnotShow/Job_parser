from aiogram import types, Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.payload import decode_payload
from dependency_injector.wiring import inject, Provide

from bot_create import bot
from src.api.applications.containers.application_service_container import ApplicationServiceContainer
from src.api.users.containers.user_service_container import UserServiceContainer
from src.api.users.user_dto import UserSettingsDTO
from src.api.applications.application_service import ApplicationService
from src.api.users.user_service import UserService
from src.bot.filters.text_filter import TextFilter
from src.bot.keyboards.main_menu_keyboard_buttons import get_main_manu_keyboard
from src.bot.localization.languages import get_main_manu_lang, get_referrals_lang, get_statistics_lang

main_manu_router = Router()


@main_manu_router.message(CommandStart())
@inject
async def main_manu(
        message: types.Message,
        command: CommandObject,
        settings: UserSettingsDTO,
        user_service: UserService = Provide[UserServiceContainer.user_service]
):
    if settings is None:
        ref = None
        if command.args:
            payload = decode_payload(command.args)
            if payload.startswith("ref="):
                ref = payload.split("=")[1]
        await user_service.create_user_from_telegram(message, ref)
    await message.answer(
        text=get_main_manu_lang(
            settings.selected_language or settings.language_code if settings else message.from_user.language_code,
            'command_start',
            message
        ),
        reply_markup=get_main_manu_keyboard(
            settings.selected_language or settings.language_code if settings else message.from_user.language_code
        )
    )


@main_manu_router.message(TextFilter(text_list=get_main_manu_keyboard(return_buttons_list=True, button='referrals')))
@inject
async def get_referrals(
        message: types.Message,
        settings: UserSettingsDTO,
        user_service: UserService = Provide[UserServiceContainer.user_service],
):
    user = await user_service.get_user_by_telegram_id(message.from_user.id)
    ref_link = await create_start_link(bot, f"ref={user.id}", encode=True)
    referrals_count = await user_service.get_user_referrals(refer_id=user.id, count=True)
    await message.answer(
        text=get_referrals_lang(settings.language_code, 'referrals', ref_link, referrals_count),
        reply_markup=get_main_manu_keyboard(settings.selected_language or settings.language_code)
    )


@main_manu_router.message(TextFilter(text_list=get_main_manu_keyboard(return_buttons_list=True, button='statistics')))
@inject
async def statistics(
        message: types.Message,
        settings: UserSettingsDTO,
        application_service: ApplicationService = Provide[ApplicationServiceContainer.application_service]
):
    jobs_counter = await application_service.get_applications_by_telegram_id(telegram_id=message.from_user.id)
    await message.answer(
        text=get_statistics_lang(settings.language_code, 'statistics', jobs_counter.total),
        reply_markup=get_main_manu_keyboard(settings.selected_language or settings.language_code)
    )
