from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from parsers import base_urls
from src.bot.keyboards.searches_menu_keyboard import get_searches_menu_keyboard, SearchesCallbackData
from src.bot.states.add_search_state import FSMSearchAddState

searches_router = Router()


@searches_router.message(F.text == "Поисковые запросы")
async def searches_menu(message: types.Message):
    await message.answer('Что хочешь сделать?', reply_markup=get_searches_menu_keyboard())


@searches_router.callback_query(SearchesCallbackData.filter(F.callback == "searches_list"))
async def searches_list(callback_query: types.CallbackQuery):
    # TODO: get from database
    await callback_query.message.answer("Не реализовано")


class AddSearch:

    @staticmethod
    @searches_router.callback_query(SearchesCallbackData.filter(F.callback == "add_search"))
    async def start(message: types.Message, state: FSMContext):
        await message.answer('Отправь ссылку на поисковой запрос для olx.pl или pracuj.pl')
        await state.set_state(FSMSearchAddState.url)

    @staticmethod
    async def get_url(message: types.Message, state: FSMContext):
        for i in base_urls:
            if message.text.startswith(i):
                await state.update_data(url=message.text)
                await message.answer('Напиши название поискового запроса')
                await state.set_state(FSMSearchAddState.title)
                break

        await message.answer('Данный ресурс не поддерживается')

    @staticmethod
    async def get_title(message: types.Message, state: FSMContext):
        await state.update_data(title=message.text)
        data = await state.get_data()
        await state.clear()
        return data
        # TODO database transaction


class DeleteSearch:

    @staticmethod
    async def start(message: types.Message, state: FSMContext):
        await message.answer('Отправь id или название поискового запроса для удаления из базы данных')

    @staticmethod
    async def process_deleting(message: types.Message, state: FSMContext):
        try:
            if message.text.isdigit():
                return await DeleteSearch._delete_request_by_id(int(message.text))
            else:
                return await DeleteSearch._delete_request_by_title(message.text)
        except Exception:
            await message.answer('Такого поискового запроса нет в базе данных')

    @staticmethod
    async def _delete_request_by_id(search_id: int):
        pass
        # TODO database transaction

    @staticmethod
    async def _delete_request_by_title(title: str):
        pass
        # TODO database transaction
