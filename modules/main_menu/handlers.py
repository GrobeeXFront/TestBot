from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove  # Добавляем импорт
from aiogram.filters import Command
from .keyboards import get_main_menu_kb, get_back_only_kb
from .texts import MainMenuTexts, AboutServiceTexts

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    user_name = message.from_user.full_name
    await message.answer(
        text=MainMenuTexts.welcome(user_name),
        reply_markup=get_main_menu_kb()
    )

@router.message(F.text == MainMenuTexts.ABOUT)
async def about_service_handler(message: Message):
    await message.answer(
        text=AboutServiceTexts.description(),
        reply_markup=get_back_only_kb(),
        parse_mode='HTML'
    )

@router.message(F.text == MainMenuTexts.BACK)
async def back_handler(message: Message):
    user_name = message.from_user.full_name
    await message.answer(
        text=MainMenuTexts.welcome(user_name),
        reply_markup=get_main_menu_kb()
    )

@router.message(F.text == MainMenuTexts.ORDER_TAXI)
async def order_taxi_handler(message: Message):
    await message.answer(
        text="Переходим к оформлению заказа...",
        reply_markup=ReplyKeyboardRemove()  # Теперь импортирован правильно
    )
    # Здесь будет автоматический переход в модуль orders