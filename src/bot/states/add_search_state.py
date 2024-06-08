from aiogram.fsm.state import State, StatesGroup


class FSMSearchAddState(StatesGroup):
    url = State()
    title = State()
