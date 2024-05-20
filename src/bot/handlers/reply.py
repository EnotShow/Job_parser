from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.markdown import hlink, hbold

from core.db.db_helper import db_helper
from src.bot.filters.callbackquery_filter import ReplyCallback, ReplyType
from src.bot.keyboards.reply_keyboard_buttons import ReplyCallbackButtons
from src.api.repositories.application_repository import ApplicationRepository

router = Router()


def new_offer(title, url, search_title):
    return f"Появился новый офер:\n{title}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}"


def offer_title(title, url, search_title):
    return f"{title}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}"


def offer_description(description, url, search_title):
    return f"{description}\n{hlink('Ссылка', url)}\nЗапрос: {hbold(search_title)}"


@router.message(Command('help'))
async def help_command(message: types.Message):
    await message.reply("Пока нет команд")


@router.callback_query(ReplyCallback.filter(F.type == ReplyType.DESCRIPTION))
async def description_reply(query: types.CallbackQuery, callback_data: ReplyCallback):
    async with db_helper.get_db_session() as session:
        application_repository = ApplicationRepository(session)
        application = await application_repository.get_by_id(callback_data.application_id)
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
async def title_reply(query: types.CallbackQuery, callback_data: ReplyCallback):
    async with db_helper.get_db_session() as session:
        application_repository = ApplicationRepository(session)
        application = await application_repository.get_by_id(callback_data.application_id)
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
