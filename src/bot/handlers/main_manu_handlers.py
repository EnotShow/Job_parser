import ast
import json

from aiogram import types, Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.markdown import hlink
from aiogram.utils.payload import decode_payload
from dependency_injector.wiring import inject, Provide

from core.config.bot import settings_bot
from src.api.applications.application_service import ApplicationService
from src.api.applications.containers.application_service_container import ApplicationServiceContainer
from src.api.auth.containers.auth_service_container import AuthServiceContainer
from src.api.auth.services.auth_service import AuthService
from src.api.messangers.bots_containers.telegram_container import TelegramServiceContainer
from src.api.messangers.bots_services.telegram_service import TelegramService
from src.api.messangers.dtos.telegram_dto import TelegramPayloadDTO
from src.api.users.containers.user_service_container import UserServiceContainer
from src.api.users.user_dto import UserSettingsDTO
from src.api.users.user_service import UserService
from src.bot.filters.text_filter import TextFilter
from src.bot.keyboards.main_menu_keyboard_buttons import get_main_manu_keyboard
from src.bot.localization.languages import get_main_manu_lang, get_referrals_lang, get_statistics_lang

main_manu_router = Router()


@main_manu_router.message(CommandStart())
@inject
async def start_bot(
        message: types.Message,
        command: CommandObject,
        settings: UserSettingsDTO,
        user_service: UserService = Provide[UserServiceContainer.user_service]
):
    payload = None
    if command.args:
        payload_json = decode_payload(command.args)
        payload = ast.literal_eval(payload_json)

    if settings is None:
        ref = None
        if payload and payload['ref'] and payload['ref'].isdigit():
            ref = int(payload['ref'])

        await user_service.create_user_from_telegram(message, ref)

    if settings and payload and payload['login']:
        return await site_login(message, settings)

    elif payload and payload['login']:
        await site_login(message, settings)

    await main_manu(message, settings)


async def main_manu(message: types.Message, settings: UserSettingsDTO = None):
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


@inject
async def site_login(
        message: types.Message,
        settings: UserSettingsDTO,
        auth_service: AuthService = Provide[AuthServiceContainer.auth_service],
):
    try:
        user_id = settings.user_id
        _hash = await auth_service.generate_login_hash(user_id)
        message_to_send = (f"{get_main_manu_lang(settings.language_code, 'auth', message)}\n"
                           f"{f"{settings_bot.frontend_url}/login/{_hash.pk}"}")
        await message.answer(message_to_send)
    except Exception as e:
        print(e)


@main_manu_router.message(TextFilter(text_list=get_main_manu_keyboard(return_buttons_list=True, button='referrals')))
@inject
async def get_referrals(
        message: types.Message,
        settings: UserSettingsDTO,
        user_service: UserService = Provide[UserServiceContainer.user_service],
        telegram_service: TelegramService = Provide[TelegramServiceContainer.telegram_service],
):
    user = await user_service.get_user_by_telegram_id(message.from_user.id)
    payload_dto = TelegramPayloadDTO(ref=user.id, login=None)
    payload = await telegram_service.encode_payload(payload_dto)
    referrals_count = await user_service.get_user_referrals(refer_id=user.id, count=True)
    await message.answer(
        text=get_referrals_lang(settings.selected_language, 'referrals', payload['start_link'], referrals_count),
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
        text=get_statistics_lang(settings.selected_language, 'statistics', jobs_counter.total),
        reply_markup=get_main_manu_keyboard(settings.selected_language or settings.language_code)
    )
