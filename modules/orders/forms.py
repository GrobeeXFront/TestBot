from aiogram.fsm.state import StatesGroup, State

class OrderForm(StatesGroup):
    POINT_A = State()
    POINT_B = State()
    EDIT_POINT_A = State()
    EDIT_POINT_B = State()
    CONFIRM = State()