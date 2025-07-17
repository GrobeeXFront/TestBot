from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .texts import Buttons

def profile_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=Buttons.HISTORY)],
            [KeyboardButton(text=Buttons.EDIT)],
            [KeyboardButton(text=Buttons.BACK)]
        ],
        resize_keyboard=True
    )

def edit_profile_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=Buttons.EDIT_NAME), KeyboardButton(text=Buttons.EDIT_PHONE)],
            [KeyboardButton(text=Buttons.EDIT_LOCATION)],
            [KeyboardButton(text=Buttons.CANCEL)]
        ],
        resize_keyboard=True
    )

def cancel_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=Buttons.CANCEL)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )