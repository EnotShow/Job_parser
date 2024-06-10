from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup
from dependency_injector.wiring import Provide

from src.api.containers.services_containers.application_service_container import ApplicationServiceContainer
from src.api.services.application_service import ApplicationService
from src.bot.filters.callbackquery_filter import ReplyCallback, ReplyType
from src.bot.handlers.base import offer_description, offer_title
from src.bot.keyboards.reply_keyboard_buttons import ReplyCallbackButtons

router = Router()


@router.message(Command('help'))
async def help_command(message: types.Message):
    await message.reply("Пока нет команд")


@router.callback_query(ReplyCallback.filter(F.type == ReplyType.DESCRIPTION))
async def description_reply(
        query: types.CallbackQuery,
        callback_data: ReplyCallback,
        application_service: ApplicationService = Provide[ApplicationServiceContainer.application_service],
):
    application = await application_service.get_application(callback_data.application_id)
    reply_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[
        ReplyCallbackButtons.button_title(
            callback_data.application_id, callback_data.search_title),
        ReplyCallbackButtons.button_apply(
            callback_data.application_id, callback_data.search_title)
    ]])
    await query.message.edit_text(
        offer_description(application.description, application.url, callback_data.search_title),
        reply_markup=reply_keyboard
    )


@router.callback_query(ReplyCallback.filter(F.type == ReplyType.TITLE))
async def title_reply(
        query: types.CallbackQuery,
        callback_data: ReplyCallback,
        application_service: ApplicationService = Provide[ApplicationServiceContainer.application_service],
):
    application = await application_service.get_application(callback_data.application_id)
    reply_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[
        ReplyCallbackButtons.button_description(
            callback_data.application_id, callback_data.search_title),
        ReplyCallbackButtons.button_apply(
            callback_data.application_id, callback_data.search_title)
    ]])
    await query.message.edit_text(
        offer_title(application.title, application.url, callback_data.search_title),
        reply_markup=reply_keyboard
    )


@router.callback_query(ReplyCallback.filter(F.type == ReplyType.APPLY))
async def apply_reply(query: types.CallbackQuery, callback_data: ReplyCallback):
    await query.answer("Not implemented yet")
