from aiogram.fsm.state import StatesGroup, State

class DriverForm(StatesGroup):
    NAME = State()
    CAR_MODEL = State()
    CAR_COLOR = State()
    CAR_NUMBER = State()
    PHONE = State()
    TELEGRAM = State()

class EditDriverForm(StatesGroup):
    TELEGRAM = State()
    FIELD = State()
    VALUE = State()
    NEW_TELEGRAM = State()

class DeleteDriverForm(StatesGroup):
    TELEGRAM = State()