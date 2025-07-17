from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from config import Config
from .keyboards import admin_kb, edit_fields_kb
from .services import DriverService
from .models import Driver
from .forms import DriverForm, EditDriverForm, DeleteDriverForm
from .texts import *

router = Router()

async def show_main_menu(message: Message):
    """Локальная функция для показа главного меню"""
    from modules.main_menu.keyboards import get_main_menu_kb
    
    await message.answer(
        "Вы в Главном меню",
        reply_markup=get_main_menu_kb()
    )

# ========== Команда /admin ==========
@router.message(Command("admin"))
async def admin_command(message: Message):
    """Обработчик команды /admin"""
    await admin_panel(message)

# ========== Главное меню ========== #
@router.message(F.text == "🔙 Главное меню")
async def back_to_menu(message: Message):
    """Возврат в главное меню"""
    await show_main_menu(message)

# ========== Админ-панель ========== #
async def admin_panel(message: Message):
    """Показывает админ-панель только администраторам"""
    if message.from_user.id not in Config.ADMIN_IDS:
        await show_main_menu(message)
        return
    
    await message.answer(ADMIN_PANEL_TITLE, reply_markup=admin_kb())

# ========== Добавление водителя ==========
@router.message(F.text == "➕ Добавить водителя")
async def add_driver_start(message: Message, state: FSMContext):
    if message.from_user.id not in Config.ADMIN_IDS:
        return await message.answer(ACCESS_DENIED)
    
    await state.set_state(DriverForm.NAME)
    await message.answer(ENTER_NAME, reply_markup=ReplyKeyboardRemove())

@router.message(DriverForm.NAME)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(DriverForm.CAR_MODEL)
    await message.answer(ENTER_CAR_MODEL)

@router.message(DriverForm.CAR_MODEL)
async def process_car_model(message: Message, state: FSMContext):
    await state.update_data(car_model=message.text)
    await state.set_state(DriverForm.CAR_COLOR)
    await message.answer(ENTER_CAR_COLOR)

@router.message(DriverForm.CAR_COLOR)
async def process_car_color(message: Message, state: FSMContext):
    await state.update_data(car_color=message.text)
    await state.set_state(DriverForm.CAR_NUMBER)
    await message.answer(ENTER_CAR_NUMBER)

@router.message(DriverForm.CAR_NUMBER)
async def process_car_number(message: Message, state: FSMContext):
    await state.update_data(car_number=message.text)
    await state.set_state(DriverForm.PHONE)
    await message.answer(ENTER_PHONE)

@router.message(DriverForm.PHONE)
async def process_phone(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer(INVALID_PHONE)
    
    await state.update_data(phone=message.text)
    await state.set_state(DriverForm.TELEGRAM)
    await message.answer(ENTER_TELEGRAM)

@router.message(DriverForm.TELEGRAM)
async def process_telegram(message: Message, state: FSMContext):
    telegram = message.text.replace("@", "").strip()
    if not telegram:
        return await message.answer(INVALID_TELEGRAM)
    
    if await DriverService.is_telegram_exists(telegram):
        return await message.answer(TELEGRAM_EXISTS)
    
    data = await state.get_data()
    try:
        driver = Driver(
            name=data['name'],
            car_model=data['car_model'],
            car_color=data['car_color'],
            car_number=data['car_number'],
            phone=data['phone'],
            telegram=telegram
        )
        driver_id = await DriverService.create_driver(driver)
        
        await message.answer(
            DRIVER_ADDED.format(
                driver_id=driver_id,
                name=driver.name,
                car_model=driver.car_model,
                car_color=driver.car_color,
                car_number=driver.car_number,
                phone=driver.phone,
                telegram=driver.telegram
            ),
            reply_markup=admin_kb()
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}", reply_markup=admin_kb())
    await state.clear()

# ========== Редактирование водителя ==========
@router.message(F.text == "✏️ Редактировать водителя")
async def edit_driver_start(message: Message, state: FSMContext):
    if message.from_user.id not in Config.ADMIN_IDS:
        return await message.answer(ACCESS_DENIED)
    
    await state.set_state(EditDriverForm.TELEGRAM)
    await message.answer(ENTER_EDIT_TELEGRAM, reply_markup=ReplyKeyboardRemove())

@router.message(EditDriverForm.TELEGRAM)
async def process_edit_telegram(message: Message, state: FSMContext):
    telegram = message.text.replace("@", "").strip()
    driver = await DriverService.get_driver_by_telegram(telegram)
    
    if not driver:
        await message.answer(DRIVER_NOT_FOUND, reply_markup=admin_kb())
        return await state.clear()
    
    await state.update_data(
        driver_id=driver['id'],
        current_telegram=driver['telegram'],
        current_name=driver['name'],
        current_car_model=driver['car_model'],
        current_car_color=driver['car_color'],
        current_car_number=driver['car_number'],
        current_phone=driver['phone_number']
    )
    
    await state.set_state(EditDriverForm.FIELD)
    await message.answer(
        EDIT_DRIVER_INFO.format(
            telegram=driver['telegram'],
            name=driver['name'],
            car_model=driver['car_model'],
            car_color=driver['car_color'],
            car_number=driver['car_number'],
            phone_number=driver['phone_number']
        ),
        reply_markup=edit_fields_kb()
    )

@router.message(EditDriverForm.FIELD)
async def process_edit_field(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await state.clear()
        return await admin_panel(message)
    
    field_map = {
        "1": {"db_field": "name", "display": "имя"},
        "2": {"db_field": "car_model", "display": "марка авто"},
        "3": {"db_field": "car_color", "display": "цвет авто"},
        "4": {"db_field": "car_number", "display": "гос. номер"},
        "5": {"db_field": "phone_number", "display": "телефон"},
        "6": {"db_field": "telegram", "display": "Telegram"}
    }
    
    choice = message.text.split()[0]  # Берем только цифру (первый символ)
    if choice not in field_map:
        return await message.answer(INVALID_FIELD_CHOICE)
    
    field_data = field_map[choice]
    await state.update_data(
        db_field=field_data["db_field"],
        display_field=field_data["display"]
    )
    
    if field_data["db_field"] == "telegram":
        await state.set_state(EditDriverForm.NEW_TELEGRAM)
        await message.answer(ENTER_NEW_TELEGRAM, reply_markup=ReplyKeyboardRemove())
    else:
        await state.set_state(EditDriverForm.VALUE)
        await message.answer(
            f"✏️ Введите новое значение для {field_data['display']}:",
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(EditDriverForm.VALUE)
async def process_edit_value(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        db_field = data['db_field']
        display_field = data['display_field']
        old_value = data[f'current_{db_field}'] if db_field != 'phone_number' else data['current_phone']
        new_value = message.text
        
        await DriverService.update_driver(
            data['driver_id'],
            **{db_field: new_value}
        )
        
        await message.answer(
            f"✅ Ваша <b>{display_field}</b> было изменено с <code>{old_value}</code> на <code>{new_value}</code>!",
            reply_markup=admin_kb()
        )
    except Exception as e:
        await message.answer(
            UPDATE_ERROR.format(error=e),
            reply_markup=admin_kb()
        )
    await state.clear()

@router.message(EditDriverForm.NEW_TELEGRAM)
async def process_new_telegram(message: Message, state: FSMContext):
    new_telegram = message.text.replace("@", "").strip()
    data = await state.get_data()
    
    if await DriverService.is_telegram_exists(new_telegram, exclude_id=data['driver_id']):
        await message.answer(TELEGRAM_TAKEN, reply_markup=admin_kb())
        return await state.clear()
    
    try:
        await DriverService.update_driver(
            data['driver_id'],
            telegram=new_telegram
        )
        await message.answer(
            TELEGRAM_UPDATED.format(
                old_telegram=data['current_telegram'],
                new_telegram=new_telegram
            ),
            reply_markup=admin_kb()
        )
    except Exception as e:
        await message.answer(UPDATE_ERROR.format(error=e), reply_markup=admin_kb())
    await state.clear()

# ========== Удаление водителя ==========
@router.message(F.text == "🗑️ Удалить водителя")
async def delete_driver_start(message: Message, state: FSMContext):
    if message.from_user.id not in Config.ADMIN_IDS:
        return await message.answer(ACCESS_DENIED)
    
    await state.set_state(DeleteDriverForm.TELEGRAM)
    await message.answer(ENTER_DELETE_TELEGRAM, reply_markup=ReplyKeyboardRemove())

@router.message(DeleteDriverForm.TELEGRAM)
async def process_delete_telegram(message: Message, state: FSMContext):
    telegram = message.text.replace("@", "").strip()
    driver = await DriverService.get_driver_by_telegram(telegram)
    
    if not driver:
        await message.answer(DRIVER_NOT_FOUND, reply_markup=admin_kb())
        return await state.clear()
    
    try:
        await DriverService.delete_driver(driver['id'])
        await message.answer(
            DRIVER_DELETED.format(
                telegram=telegram,
                name=driver['name'],
                car_model=driver['car_model'],
                car_color=driver['car_color']
            ),
            reply_markup=admin_kb()
        )
    except Exception as e:
        await message.answer(DELETE_ERROR.format(error=e), reply_markup=admin_kb())
    await state.clear()