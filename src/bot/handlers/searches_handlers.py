from typing import List

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import inject, Provide

from core.shared.errors import ResourceError
from core.shared.validators import JobResourceURL
from src.api.searches.containers.search_service_container import SearchServiceContainer
from src.api.searches.search_dto import SearchDTO, SearchUpdateDTO
from src.api.users.user_dto import UserSettingsDTO
from src.api.searches.searchings_service import SearchService
from src.bot.filters.text_filter import TextFilter
from src.bot.keyboards.main_menu_keyboard_buttons import get_main_manu_keyboard
from src.bot.keyboards.searches_menu_keyboard import get_searches_menu_keyboard, SearchesCallbackData, \
    get_searches_list_menu_keyboard
from src.bot.localization.languages import get_searches_lang
from src.bot.states.search_states import FSMSearchAddState, FSMSearchDeleteState

searches_router = Router()


@searches_router.message(TextFilter(text_list=get_main_manu_keyboard(return_buttons_list=True, button='searches')))
async def searches_menu(message: types.Message, settings: UserSettingsDTO):
    await message.answer(
        get_searches_lang(
            settings.selected_language or settings.selected_language,
            'searches_manu'
        ),
        reply_markup=get_searches_menu_keyboard(settings.selected_language or settings.selected_language)
    )


@searches_router.callback_query(SearchesCallbackData.filter(F.callback == "searches_list"))
@inject
async def searches_list(
        callback_query: types.CallbackQuery,
        settings: UserSettingsDTO,
        search_service: SearchService = Provide[SearchServiceContainer.search_service],
):
    searches: List[SearchDTO] = await search_service.get_telegram_user_searches(callback_query.from_user.id)
    if searches:
        for search in searches:
            await callback_query.message.answer(
                f'{search.title}\n{search.url}',
                reply_markup=get_searches_list_menu_keyboard(
                    search.id,
                    settings.selected_language or settings.selected_language
                ))
    else:
        await callback_query.message.answer(get_searches_lang(
            settings.selected_language or settings.selected_language,
            'no_resources'
        ))
    # await callback_query.message.answer('Вернуться назад?', reply_markup=None)  # TODO add back byttton


@searches_router.callback_query(SearchesCallbackData.filter(F.callback == "delete_search"))
@inject
async def delete_search(
        callback_query: types.CallbackQuery,
        callback_data: SearchesCallbackData,
        settings: UserSettingsDTO,
        search_service: SearchService = Provide[SearchServiceContainer.search_service],
):
    await search_service.delete_search(callback_data.search_id)
    await callback_query.message.delete()
    await callback_query.answer(
        get_searches_lang(
            settings.selected_language or settings.selected_language,
            'resource_deleted')
    )


class AddSearch:

    @staticmethod
    @searches_router.callback_query(SearchesCallbackData.filter(F.callback == "add_search"))
    async def start(
            callback_query: types.CallbackQuery,
            state: FSMContext,
            settings: UserSettingsDTO,
    ):
        await callback_query.message.answer(get_searches_lang(
            settings.selected_language or settings.selected_language,
            'resource_url'
        ))
        await state.set_state(FSMSearchAddState.url)

    @staticmethod
    @searches_router.message(FSMSearchAddState.url)
    async def get_url(
            message: types.Message,
            state: FSMContext,
            settings: UserSettingsDTO,
    ):
        try:
            resource_validate = JobResourceURL.validate(message.text)
            if resource_validate:
                await state.update_data(url=message.text)
                await message.answer(
                    get_searches_lang(
                        settings.selected_language or settings.selected_language,
                        'resource_title'
                    )
                )
                await state.set_state(FSMSearchAddState.title)
        except ResourceError as e:
            await message.answer(
                get_searches_lang(
                    settings.selected_language or settings.selected_language,
                    'unsupported_resource',
                )
            )

    @staticmethod
    @searches_router.message(FSMSearchAddState.title)
    @inject
    async def get_title(
            message: types.Message,
            state: FSMContext,
            settings: UserSettingsDTO,
            search_service: SearchService = Provide[SearchServiceContainer.search_service],
    ):
        await state.update_data(title=message.text)
        data = await state.get_data()
        await search_service.crete_search_from_telegram(data=data, telegram_id=message.from_user.id)
        await state.clear()
        await message.answer(get_searches_lang(
            settings.selected_language or settings.selected_language,
            'resource_added'
        ))


class ChangeSearch:
    @staticmethod
    @searches_router.callback_query(SearchesCallbackData.filter(F.callback == "change_search"))
    async def start(
            callback_query: types.CallbackQuery,
            callback_data: SearchesCallbackData,
            state: FSMContext,
            settings: UserSettingsDTO,
    ):
        await state.set_state(FSMSearchDeleteState.url)
        await state.update_data(search_id=callback_data.search_id)
        await callback_query.message.answer(get_searches_lang(
            settings.selected_language or settings.selected_language,
            'resource_new_link'
        ))

    @staticmethod
    @searches_router.message(FSMSearchDeleteState.url)
    @inject
    async def change_search(
            message: types.Message,
            state: FSMContext,
            settings: UserSettingsDTO,
            search_service: SearchService = Provide[SearchServiceContainer.search_service],
    ):
        try:
            resource_validate = JobResourceURL.validate(message.text)
            if resource_validate:
                data = await state.get_data()
                search_obj = SearchUpdateDTO(
                    id=data['search_id'],
                    url=message.text,
                )
                await search_service.update_search(search_obj)
                await state.clear()
                await message.answer(get_searches_lang(
                    settings.selected_language or settings.selected_language,
                    'resource_changed'
                ))
        except ResourceError as e:
            await message.answer(get_searches_lang(
                settings.selected_language or settings.selected_language,
                'unsupported_resource'
            ))
