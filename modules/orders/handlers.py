from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging
from config import Config

from .keyboards import (
    order_start_kb,
    order_edit_points_kb,
    order_confirm_kb,
    cancel_kb,
    driver_actions_kb
)
from .services import OrderService
from .models import Order
from .forms import OrderForm
from modules.clients.services import ClientService
from .driver import DriverService
from .texts import OrderTexts

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

router = Router()

async def get_order_accepted_message(order_id: int, driver_username: str, order_data: dict = None) -> str:
    """Формирует сообщение о принятом заказе"""
    if not order_data:
        order = await OrderService.get_order(order_id)
        if not order:
            return None
        
        client = await ClientService.get_client_by_id(order['client_id'])
        if not client:
            return None
        
        order_data = {
            'car_number': order.get('car_number', 'не указан'),
            'car_color': order.get('car_color', 'не указан'),
            'car_model': order.get('car_model', 'не указан'),
            'driver_name': order.get('driver_name', 'водитель')
        }
    
    return OrderTexts.DRIVER_ASSIGNED.format(
        order_id=order_id,
        driver_name=order_data.get('driver_name', 'водитель'),
        car_color=order_data.get('car_color', 'не указан'),
        car_model=order_data.get('car_model', 'не указан'),
        car_number=order_data.get('car_number', 'не указан'),
        driver_username=driver_username
    )

async def send_order_to_drivers_chat(order: dict, bot: Bot):
    """Отправляет заказ в чат водителей"""
    try:
        if not Config.CHATS.get('drivers'):
            logging.error("Chat ID for drivers not configured")
            return False

        text = OrderTexts.NEW_ORDER_NOTIFICATION.format(
            client_name=order['client_name'],
            client_phone=order['client_phone'],
            client_username=order['client_username'],
            pickup_location=order['pickup_location'],
            point_a=order['point_a'],
            point_b=order['point_b']
        )

        await bot.send_message(
            chat_id=Config.CHATS['drivers'],
            text=text,
            reply_markup=driver_actions_kb(order['id'])
        )
        return True

    except Exception as e:
        logging.error(f"Ошибка отправки заказа: {str(e)}")
        return False

@router.message(F.text == OrderTexts.ORDER_BUTTON)
async def start_order_handler(message: Message, state: FSMContext):
    """Обработчик начала заказа такси"""
    logging.info(f"Начало обработки заказа для пользователя {message.from_user.id}")
    
    try:
        await state.clear()
        
        client = await ClientService.get_client(message.from_user.id)
        if not client:
            logging.warning(f"Профиль не найден для пользователя {message.from_user.id}")
            await message.answer(
                OrderTexts.PROFILE_REQUIRED,
                reply_markup=ReplyKeyboardRemove()
            )
            return
        
        if not all([client.get('id'), client.get('location')]):
            logging.error(f"Неполные данные клиента: {client}")
            await message.answer(
                OrderTexts.PROFILE_REQUIRED,
                reply_markup=ReplyKeyboardRemove()
            )
            return
        
        await state.set_state(OrderForm.POINT_A)
        await state.update_data({
            'client_id': client['id'],
            'client_name': client.get('name', 'Не указано'),
            'client_phone': client.get('phone', 'Не указан'),
            'client_username': message.from_user.username or 'Не указан',
            'pickup_location': client['location']
        })
        
        logging.info(f"Переход в состояние POINT_A для пользователя {message.from_user.id}")
        await message.answer(
            OrderTexts.POINT_A_PROMPT.format(cancel_btn=OrderTexts.CANCEL_BTN),
            reply_markup=cancel_kb()
        )
        
    except Exception as e:
        logging.error(f"Ошибка в start_order_handler: {str(e)}", exc_info=True)
        await message.answer(
            OrderTexts.ORDER_ERROR.format(error="Ошибка при начале заказа"),
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(OrderForm.POINT_A)
async def process_point_a(message: Message, state: FSMContext):
    """Обработчик точки А"""
    try:
        await state.update_data(point_a=message.text)
        await state.set_state(OrderForm.POINT_B)
        
        await message.answer(
            OrderTexts.POINT_B_PROMPT.format(cancel_btn=OrderTexts.CANCEL_BTN),
            reply_markup=cancel_kb()
        )
    except Exception as e:
        logging.error(f"Ошибка в process_point_a: {str(e)}")
        await message.answer(
            OrderTexts.ORDER_ERROR.format(error="Ошибка при вводе точки А"),
            reply_markup=cancel_kb()
        )

@router.message(OrderForm.POINT_B)
async def process_point_b(message: Message, state: FSMContext):
    """Обработчик точки Б"""
    try:
        await state.update_data(point_b=message.text)
        await state.set_state(OrderForm.CONFIRM)
        
        data = await state.get_data()
        
        await message.answer(
            OrderTexts.ORDER_CONFIRMATION.format(
                pickup_location=data['pickup_location'],
                point_a=data['point_a'],
                point_b=data['point_b'],
                confirm_btn=OrderTexts.CONFIRM_ORDER_BTN
            ),
            reply_markup=order_confirm_kb()
        )
    except Exception as e:
        logging.error(f"Ошибка в process_point_b: {str(e)}")
        await message.answer(
            OrderTexts.ORDER_ERROR.format(error="Ошибка при вводе точки Б"),
            reply_markup=cancel_kb()
        )

@router.message(OrderForm.CONFIRM, F.text == OrderTexts.CONFIRM_ORDER_BTN)
async def confirm_order(message: Message, state: FSMContext, bot: Bot):
    """Подтверждение заказа"""
    if not Config.CHATS.get('drivers'):
        await message.answer(
            OrderTexts.SERVICE_UNAVAILABLE,
            reply_markup=ReplyKeyboardRemove()
        )
        return

    try:
        data = await state.get_data()
        
        order = Order(
            client_id=data['client_id'],
            pickup_location=data['pickup_location'],
            point_a=data['point_a'],
            point_b=data['point_b'],
            status='pending'
        )
        
        order_id = await OrderService.create_order(order)
        if not order_id:
            raise Exception("Не удалось создать заказ")

        order_data = {'id': order_id, **data}
        if not await send_order_to_drivers_chat(order_data, bot):
            raise Exception("Не удалось отправить заказ водителям")

        await message.answer(
            OrderTexts.ORDER_ACCEPTED,
            reply_markup=ReplyKeyboardRemove()
        )

    except Exception as e:
        await message.answer(
            OrderTexts.ORDER_ERROR.format(error=str(e)),
            reply_markup=ReplyKeyboardRemove()
        )
        logging.error(f"Ошибка создания заказа: {str(e)}")
    
    await state.clear()

@router.callback_query(F.data.startswith("accept_order_"))
async def accept_order(callback: CallbackQuery, bot: Bot):
    """Принятие заказа водителем"""
    order_id = int(callback.data.split("_")[-1])
    driver_id = callback.from_user.id
    
    try:
        await OrderService.update_order_status(order_id, "accepted")
        await OrderService.assign_driver(order_id, driver_id)
        
        order = await OrderService.get_order(order_id)
        if not order:
            raise Exception("Заказ не найден")

        client = await ClientService.get_client_by_id(order['client_id'])
        if not client or not client.get('telegram_id'):
            raise Exception("Не удалось получить данные клиента")

        driver = await DriverService.get_driver(driver_id)
        order_data = {
            'car_number': driver.get('car_number'),
            'car_color': driver.get('car_color'),
            'car_model': driver.get('car_model'),
            'driver_name': driver.get('name')
        }

        message_text = await get_order_accepted_message(
            order_id=order_id,
            driver_username=callback.from_user.username,
            order_data=order_data
        )
        
        if not message_text:
            raise Exception("Не удалось сформировать сообщение")

        await bot.send_message(
            chat_id=client['telegram_id'],
            text=message_text
        )

        await callback.message.edit_text(
            f"{callback.message.text}\n\n"
            f"{OrderTexts.ORDER_ACCEPTED_BY_DRIVER.format(username=callback.from_user.username)}",
            reply_markup=None
        )
        await callback.answer(OrderTexts.ACCEPT_ORDER_BTN)

    except Exception as e:
        await callback.answer(OrderTexts.ORDER_ERROR.format(error=str(e)))
        logging.error(f"Ошибка принятия заказа: {str(e)}")

@router.callback_query(F.data.startswith("skip_order_"))
async def skip_order(callback: CallbackQuery):
    """Пропуск заказа водителем"""
    order_id = int(callback.data.split("_")[-1])
    
    try:
        await callback.message.edit_text(
            f"{callback.message.text}\n\n"
            f"{OrderTexts.ORDER_SKIPPED}",
            reply_markup=None
        )
        await callback.answer(OrderTexts.SKIP_ORDER_BTN)
    except Exception as e:
        await callback.answer(OrderTexts.ORDER_ERROR.format(error=str(e)))
        logging.error(f"Ошибка пропуска заказа: {str(e)}")