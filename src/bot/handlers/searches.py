from typing import List

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import inject, Provide

from parsers import base_urls
from src.api.containers.services_containers.search_service_container import SearchServiceContainer
from src.api.dtos.search_dto import SearchDTO
from src.api.services.searchings_service import SearchService
from src.bot.keyboards.searches_menu_keyboard import get_searches_menu_keyboard, SearchesCallbackData, \
    get_searches_list_menu_keyboard
from src.bot.states.search_states import FSMSearchAddState, FSMSearchDeleteState

searches_router = Router()


@searches_router.message(F.text == "Поисковые запросы")
async def searches_menu(message: types.Message):
    await message.answer('Что хочешь сделать?', reply_markup=get_searches_menu_keyboard())


@searches_router.callback_query(SearchesCallbackData.filter(F.callback == "searches_list"))
@inject
async def searches_list(
        callback_query: types.CallbackQuery,
        search_service: SearchService = Provide[SearchServiceContainer.search_service],
):
    searches: List[SearchDTO] = await search_service.get_telegram_user_searches(callback_query.from_user.id)
    if searches:
        for search in searches:
            await callback_query.message.answer(
                f'{search.title}\n{search.url}',
                reply_markup=get_searches_list_menu_keyboard(search.id))
    else:
        await callback_query.message.answer('Нету поисковых запросов')
    # await callback_query.message.answer('Вернуться назад?', reply_markup=None)  # TODO add back byttton


@searches_router.callback_query(SearchesCallbackData.filter(F.callback == "delete_search"))
@inject
async def delete_search(
        callback_query: types.CallbackQuery,
        callback_data: SearchesCallbackData = Provide[SearchServiceContainer.search_service],
        search_service: SearchService = Provide[SearchServiceContainer.search_service],
):
    await search_service.delete_search(callback_data.search_id)
    await callback_query.message.delete()
    await callback_query.answer('Запись удаленна!')


class AddSearch:

    @staticmethod
    @searches_router.callback_query(SearchesCallbackData.filter(F.callback == "add_search"))
    async def start(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.answer('Отправь ссылку на поисковой запрос для olx.pl или pracuj.pl')
        await state.set_state(FSMSearchAddState.url)

    @staticmethod
    @searches_router.message(FSMSearchAddState.url)
    async def get_url(message: types.Message, state: FSMContext):
        resource_finded = False
        for i in base_urls:
            if message.text.startswith(i):
                resource_finded = True
                break
        if resource_finded:
            await state.update_data(url=message.text)
            await message.answer('Напиши название поискового запроса')
            await state.set_state(FSMSearchAddState.title)
        else:
            await message.answer('Данный ресурс не поддерживается')

    @staticmethod
    @searches_router.message(FSMSearchAddState.title)
    @inject
    async def get_title(
            message: types.Message,
            state: FSMContext,
            search_service: SearchService = Provide[SearchServiceContainer.search_service],
    ):
        await state.update_data(title=message.text)
        data = await state.get_data()
        await search_service.crete_search_from_telegram(data=data, telegram_id=message.from_user.id)
        await state.clear()
        await message.answer("Поисковой запрос создан!")


class ChangeSearch:
    @staticmethod
    @searches_router.callback_query(SearchesCallbackData.filter(F.callback == "change_search"))
    async def start(
            callback_query: types.CallbackQuery,
            callback_data: SearchesCallbackData,
            state: FSMContext,
    ):
        await state.set_state(FSMSearchDeleteState.url)
        await state.update_data(search_id=callback_data.search_id)
        await callback_query.message.answer('Отправь новую ссылку для пооискового запроса')

    @staticmethod
    @searches_router.message(FSMSearchDeleteState.url)
    @inject
    async def change_search(
            message: types.Message,
            state: FSMContext,
            search_service: SearchService = Provide[SearchServiceContainer.search_service],
    ):
        data = await state.get_data()
        search_obj = SearchDTO(id=data['search_id'], title=message.text, url=message.text)
        await search_service.update_search(search_obj)
        await state.clear()
        await message.answer('Запись обновленна!')

# class DeleteSearch:
#
#     @staticmethod
#     async def start(message: types.Message, state: FSMContext):
#         await message.answer('Отправь id или название поискового запроса для удаления из базы данных')
#
#     @staticmethod
#     async def process_deleting(message: types.Message, state: FSMContext):
#         try:
#             if message.text.isdigit():
#                 return await DeleteSearch._delete_request_by_id(int(message.text))
#             else:
#                 return await DeleteSearch._delete_request_by_title(message.text)
#         except Exception:
#             await message.answer('Такого поискового запроса нет в базе данных')
#
#     @staticmethod
#     async def _delete_request_by_id(search_id: int):
#         pass
#         # TODO database transaction
#
#     @staticmethod
#     async def _delete_request_by_title(title: str):
#         pass
#         # TODO database transaction
