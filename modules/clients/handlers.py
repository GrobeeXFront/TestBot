from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

from .keyboards import profile_kb, edit_profile_kb, cancel_kb
from .texts import ClientTexts, Buttons
from .services import ClientService
from .models import Client
from .forms import ClientForm, EditClientForm

router = Router()

@router.message(F.text == Buttons.PROFILE)
async def profile_handler(message: Message, state: FSMContext):
    await state.clear()
    client = await ClientService.get_client(message.from_user.id)
    if client:
        await message.answer(
            ClientTexts.PROFILE_TITLE + ClientTexts.PROFILE_DATA.format(
                name=client['name'],
                phone=client['phone'],
                location=client['location']
            ),
            reply_markup=profile_kb()
        )
    else:
        await state.set_state(ClientForm.NAME)
        await message.answer(
            ClientTexts.REGISTER_START,
            reply_markup=cancel_kb()
        )

@router.message(F.text == Buttons.HISTORY)
async def order_history_handler(message: Message):
    orders = []  # Здесь будет запрос к БД
    if not orders:
        await message.answer(
            ClientTexts.NO_HISTORY,
            reply_markup=profile_kb()
        )
        return
    
    text = ClientTexts.HISTORY_TITLE
    for i, order in enumerate(orders, 1):
        text += ClientTexts.HISTORY_ITEM.format(
            num=i,
            date=order['date'],
            from_loc=order['from'],
            to=order['to']
        )
    
    await message.answer(text, reply_markup=profile_kb())

@router.message(F.text == Buttons.EDIT)
async def edit_profile_start(message: Message, state: FSMContext):
    client = await ClientService.get_client(message.from_user.id)
    if not client:
        await message.answer(ClientTexts.PROFILE_NOT_FOUND)
        return
        
    await state.set_data({"client_data": client})
    await state.set_state(EditClientForm.FIELD)
    await message.answer(
        ClientTexts.EDIT_START,
        reply_markup=edit_profile_kb()
    )

@router.message(EditClientForm.FIELD, F.text == Buttons.CANCEL)
async def cancel_editing(message: Message, state: FSMContext):
    await state.clear()
    client = await ClientService.get_client(message.from_user.id)
    await message.answer(
        ClientTexts.PROFILE_TITLE + ClientTexts.PROFILE_DATA.format(
            name=client['name'],
            phone=client['phone'],
            location=client['location']
        ),
        reply_markup=profile_kb()
    )

@router.message(EditClientForm.FIELD, F.text.in_([Buttons.EDIT_NAME, Buttons.EDIT_PHONE, Buttons.EDIT_LOCATION]))
async def select_field_to_edit(message: Message, state: FSMContext):
    field_map = {
        Buttons.EDIT_NAME: ("name", "Иван Иванов"),
        Buttons.EDIT_PHONE: ("phone", "79123456789"),
        Buttons.EDIT_LOCATION: ("location", "с. Кандры")
    }
    
    field, example = field_map[message.text]
    await state.update_data(edit_field=field)
    await state.set_state(EditClientForm.VALUE)
    
    await message.answer(
        ClientTexts.EDIT_FIELD_PROMPT.format(field=field, example=example),
        reply_markup=cancel_kb()
    )

@router.message(EditClientForm.VALUE, F.text == Buttons.CANCEL)
async def cancel_value_input(message: Message, state: FSMContext):
    await state.set_state(EditClientForm.FIELD)
    await message.answer(
        ClientTexts.EDIT_CANCEL,
        reply_markup=edit_profile_kb()
    )

@router.message(EditClientForm.VALUE)
async def process_edit_value(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data['edit_field']
    new_value = message.text
    
    # Сопоставление английских названий полей с русскими
    field_names = {
        "name": "Имя",
        "phone": "Телефон",
        "location": "Город"
    }
    
    # Валидация телефона
    if field == "phone":
        if not new_value.isdigit() or len(new_value) != 11:
            await message.answer(ClientTexts.PHONE_ERROR)
            return
    
    try:
        await ClientService.update_client(
            telegram_id=message.from_user.id,
            **{field: new_value}
        )
        
        # Получаем обновлённые данные
        client = await ClientService.get_client(message.from_user.id)
        
        await message.answer(
            ClientTexts.EDIT_SUCCESS.format(field=field_names[field]),
            reply_markup=profile_kb()
        )
        
        # Показываем обновлённый профиль
        await message.answer(
            ClientTexts.PROFILE_TITLE + ClientTexts.PROFILE_DATA.format(
                name=client['name'],
                phone=client['phone'],
                location=client['location']
            ),
            reply_markup=profile_kb()
        )
        
        await state.clear()
    except Exception:
        await message.answer(
            ClientTexts.ERROR_OCCURRED,
            reply_markup=profile_kb()
        )
        await state.clear()

@router.message(F.text == Buttons.BACK)
async def back_handler(message: Message, state: FSMContext):
    await state.clear()
    client = await ClientService.get_client(message.from_user.id)
    if client:
        await message.answer(
            ClientTexts.PROFILE_TITLE + ClientTexts.PROFILE_DATA.format(
                name=client['name'],
                phone=client['phone'],
                location=client['location']
            ),
            reply_markup=profile_kb()
        )
    else:
        await message.answer(
            "Главное меню",
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(ClientForm.NAME, F.text == Buttons.CANCEL)
async def cancel_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        ClientTexts.OPERATION_CANCELED,
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(ClientForm.NAME)
async def process_name(message: Message, state: FSMContext):
    if len(message.text) < 2:
        await message.answer(ClientTexts.NAME_ERROR)
        return
        
    await state.update_data(name=message.text)
    await state.set_state(ClientForm.PHONE)
    await message.answer(
        ClientTexts.REGISTER_PHONE,
        reply_markup=cancel_kb()
    )

@router.message(ClientForm.PHONE, F.text == Buttons.CANCEL)
async def cancel_registration_phone(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        ClientTexts.OPERATION_CANCELED,
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(ClientForm.PHONE)
async def process_phone(message: Message, state: FSMContext):
    if not message.text.isdigit() or len(message.text) != 11:
        await message.answer(ClientTexts.PHONE_ERROR)
        return
        
    await state.update_data(phone=message.text)
    await state.set_state(ClientForm.LOCATION)
    await message.answer(
        ClientTexts.REGISTER_LOCATION,
        reply_markup=cancel_kb()
    )

@router.message(ClientForm.LOCATION, F.text == Buttons.CANCEL)
async def cancel_registration_location(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        ClientTexts.OPERATION_CANCELED,
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(ClientForm.LOCATION)
async def process_location(message: Message, state: FSMContext):
    if len(message.text) < 3:
        await message.answer(ClientTexts.LOCATION_ERROR)
        return
        
    data = await state.get_data()
    client = Client(
        telegram_id=message.from_user.id,
        name=data['name'],
        phone=data['phone'],
        location=message.text
    )
    
    try:
        await ClientService.create_or_update(client)
        await message.answer(
            ClientTexts.REGISTER_SUCCESS,
            reply_markup=profile_kb()
        )
    except Exception:
        await message.answer(
            ClientTexts.ERROR_OCCURRED,
            reply_markup=profile_kb()
        )
    await state.clear()