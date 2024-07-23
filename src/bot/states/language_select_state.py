from aiogram.fsm.state import State, StatesGroup


class FSMLanguageSelectState(StatesGroup):
    language = State()
