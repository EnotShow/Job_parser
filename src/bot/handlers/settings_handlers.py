from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import inject, Provide

from src.api.users.containers.user_service_container import UserServiceContainer
from src.api.users.user_dto import UserSettingsDTO, UserUpdateDTO
from src.api.users.user_service import UserService
from src.bot.filters.text_filter import TextFilter
from src.bot.keyboards.main_menu_keyboard_buttons import get_main_manu_keyboard
from src.bot.keyboards.settings_manu_keyboard import get_settings_menu_keyboard, SettingsCallbackType, \
    SettingsCallbackData, get_language_select_keyboard
from src.bot.localization.languages import get_main_manu_lang

settings_router = Router()


@settings_router.message(TextFilter(get_main_manu_keyboard(return_buttons_list=True, button="settings")))
@inject
async def settings_manu(message: types.Message, settings: UserSettingsDTO):
    await message.answer(
        text=get_main_manu_lang(settings.selected_language or settings.language_code, 'settings_menu', message),
        reply_markup=get_settings_menu_keyboard(settings),
    )


class ChangeLanguage:

    @staticmethod
    @settings_router.callback_query(SettingsCallbackData.filter(F.callback == SettingsCallbackType.LANGUAGE))
    @inject
    async def language_select(callback_query: types.CallbackQuery, state: FSMContext, settings: UserSettingsDTO):
        await callback_query.message.edit_text(
            text=get_main_manu_lang(settings.selected_language, 'settings_menu', callback_query.message),
            reply_markup=get_language_select_keyboard()
        )

    @staticmethod
    @settings_router.callback_query(SettingsCallbackData.filter(F.callback == SettingsCallbackType.CHANGE_LANGUAGE))
    @inject
    async def change_language(
            callback_query: types.CallbackQuery,
            callback_data: SettingsCallbackData,
            settings: UserSettingsDTO,
            user_service: UserService = Provide[UserServiceContainer.user_service],
    ):
        await user_service.update_user(UserUpdateDTO(
            id=settings.id,
            selected_language=callback_data.language_option
        ))
        settings.selected_language = callback_data.language_option
        await callback_query.message.delete()
        await callback_query.message.answer(
            text=get_main_manu_lang(
                callback_data.language_option,
                'settings_changed',
                callback_query.message
            ),
            reply_markup=get_main_manu_keyboard(callback_data.language_option),
        )
        await callback_query.message.answer(
            text=get_main_manu_lang(callback_data.language_option, 'settings_menu', callback_query.message),
            reply_markup=get_settings_menu_keyboard(settings)
        )


@settings_router.callback_query(SettingsCallbackData.filter(F.callback == SettingsCallbackType.PAUSING))
@inject
async def change_pausing(
        callback_query: types.CallbackQuery,
        settings: UserSettingsDTO,
        user_service: UserService = Provide[UserServiceContainer.user_service],
):
    await user_service.update_user(UserUpdateDTO(id=settings.id, paused=not settings.paused))
    await callback_query.message.edit_text(
        text=get_main_manu_lang(settings.language_code, 'settings_menu', callback_query.message),
        reply_markup=get_settings_menu_keyboard(settings)
    )
