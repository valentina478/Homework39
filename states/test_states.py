from aiogram.dispatcher.filters.state import State, StatesGroup

class TestStates(StatesGroup):
    first_q = State()
    second_q = State()
    third_q = State()
    result = State()
    choice = State()
    i_m_d = State()
    exit = State()