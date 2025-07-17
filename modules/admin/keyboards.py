from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import Config

def admin_kb():
    """Клавиатура админ-панели (только для админов)"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить водителя"), KeyboardButton(text="✏️ Редактировать водителя")],
            [KeyboardButton(text="🗑️ Удалить водителя")],
            [KeyboardButton(text="🔙 Главное меню")]
        ],
        resize_keyboard=True
    )

def edit_fields_kb():
    """Клавиатура выбора поля для редактирования"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1"), KeyboardButton(text="2")],  # Просто цифры
            [KeyboardButton(text="3"), KeyboardButton(text="4")],
            [KeyboardButton(text="5"), KeyboardButton(text="6")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )