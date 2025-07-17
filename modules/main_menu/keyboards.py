from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import Config
from .texts import MainMenuTexts

def get_main_menu_kb() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text=MainMenuTexts.PROFILE)],
        [KeyboardButton(text=MainMenuTexts.ORDER_TAXI)],
        [KeyboardButton(text=MainMenuTexts.ABOUT)]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_back_only_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=MainMenuTexts.BACK)]],
        resize_keyboard=True
    )