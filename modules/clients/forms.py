from aiogram.fsm.state import StatesGroup, State

class ClientForm(StatesGroup):
    NAME = State()
    PHONE = State()
    LOCATION = State()

class EditClientForm(StatesGroup):
    FIELD = State()
    VALUE = State()