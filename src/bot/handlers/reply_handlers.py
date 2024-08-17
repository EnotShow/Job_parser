from aiogram import types, Router, F
from aiogram.types import InlineKeyboardMarkup
from dependency_injector.wiring import Provide, inject

from src.api.applications.containers.application_service_container import ApplicationServiceContainer
from src.api.users.user_dto import UserSettingsDTO
from src.api.applications.application_service import ApplicationService
from src.bot.filters.callbackquery_filter import ReplyCallback, ReplyType
from src.bot.handlers.base_handlers import offer_description, offer_title
from src.bot.keyboards.reply_keyboard_buttons import ReplyCallbackButtons

router = Router()


@router.callback_query(ReplyCallback.filter(F.type == ReplyType.DESCRIPTION))
@inject
async def description_reply(
        query: types.CallbackQuery,
        callback_data: ReplyCallback,
        settings: UserSettingsDTO,
        application_service: ApplicationService = Provide[ApplicationServiceContainer.application_service],
):
    try:
        application = await application_service.get_application(callback_data.application_id)
        reply_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[
            ReplyCallbackButtons.button_title(
                callback_data.application_id,
                callback_data.search_title,
                settings.selected_language or settings.language_code
            ),
            ReplyCallbackButtons.button_apply(
                callback_data.application_id,
                callback_data.search_title,
                settings.selected_language or settings.language_code
            )
        ]])
        await query.message.edit_text(
            offer_description(
                application.description, application.url, callback_data.search_title, settings.selected_language),
            reply_markup=reply_keyboard
        )
    except Exception as e:
        print(e)


@router.callback_query(ReplyCallback.filter(F.type == ReplyType.TITLE))
@inject
async def title_reply(
        query: types.CallbackQuery,
        callback_data: ReplyCallback,
        settings: UserSettingsDTO,
        application_service: ApplicationService = Provide[ApplicationServiceContainer.application_service],
):
    application = await application_service.get_application(callback_data.application_id)
    reply_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[
        ReplyCallbackButtons.button_description(
            callback_data.application_id,
            callback_data.search_title,
            settings.selected_language or settings.language_code
        ),
        ReplyCallbackButtons.button_apply(
            callback_data.application_id,
            callback_data.search_title,
            settings.selected_language or settings.language_code
        )
    ]])
    await query.message.edit_text(
        offer_title(
            application.title, application.url, callback_data.search_title, settings.selected_language),
        reply_markup=reply_keyboard
    )
