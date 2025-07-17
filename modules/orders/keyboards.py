from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from .texts import OrderTexts

def order_start_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=OrderTexts.ORDER_BUTTON)]],
        resize_keyboard=True
    )

def order_confirm_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=OrderTexts.EDIT_POINT_A_BTN), 
             KeyboardButton(text=OrderTexts.EDIT_POINT_B_BTN)],
            [KeyboardButton(text=OrderTexts.CONFIRM_ORDER_BTN)],
            [KeyboardButton(text=OrderTexts.CANCEL_ORDER_BTN)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def order_edit_points_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=OrderTexts.EDIT_POINT_A_BTN),
             KeyboardButton(text=OrderTexts.EDIT_POINT_B_BTN)],
            [KeyboardButton(text=OrderTexts.CANCEL_BTN)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=OrderTexts.CANCEL_BTN)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def driver_actions_kb(order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=OrderTexts.ACCEPT_ORDER_BTN, callback_data=f"accept_order_{order_id}"),
            InlineKeyboardButton(text=OrderTexts.SKIP_ORDER_BTN, callback_data=f"skip_order_{order_id}")
        ]]
    )