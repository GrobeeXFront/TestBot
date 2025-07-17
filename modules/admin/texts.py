# Тексты админ-панели
ADMIN_PANEL_TITLE = """👨‍💻 <b>Административная панель</b>

Здесь вы можете управлять водителями"""
ACCESS_DENIED = "⛔ <b>Доступ запрещён!</b>\nУ вас нет прав администратора"
MENU_ITEM = "👨‍💻 Админка"

# Добавление водителя
ENTER_NAME = "✏️ Введите <b>имя водителя</b>:"
ENTER_CAR_MODEL = "🚗 Введите <b>марку автомобиля</b>:"
ENTER_CAR_COLOR = "🎨 Введите <b>цвет автомобиля</b>:"
ENTER_CAR_NUMBER = "🔢 Введите <b>государственный номер</b> (например, А123БВ777):"
ENTER_PHONE = "📞 Введите <b>номер телефона</b> (только цифры, например 79123456789):"
ENTER_TELEGRAM = "📱 Введите <b>Telegram username</b> (без @, например <code>ivanov</code>):"
INVALID_PHONE = """❌ <b>Неверный формат телефона!</b>

Используйте только цифры, например:
<code>79123456789</code>"""
INVALID_TELEGRAM = """❌ <b>Неверный Telegram username!</b>

Введите без @, например:
<code>ivanov</code>"""
TELEGRAM_EXISTS = "❌ <b>Водитель с таким Telegram уже существует!</b>"
DRIVER_ADDED = """✅ <b>Водитель успешно добавлен!</b>

📋 <b>Данные водителя:</b>
├ ID: <code>{driver_id}</code>
├ 👤 Имя: <code>{name}</code>
├ 🚗 Авто: {car_model} ({car_color})
├ 🔢 Номер: <code>{car_number}</code>
├ 📞 Телефон: <code>{phone}</code>
└ 📱 Telegram: @{telegram}"""

# Редактирование водителя
ENTER_EDIT_TELEGRAM = """✏️ <b>Редактирование водителя</b>

Введите Telegram username водителя (без @):"""
DRIVER_NOT_FOUND = """❌ <b>Водитель не найден!</b>

Проверьте правильность ввода"""
EDIT_DRIVER_INFO = """✏️ <b>Редактирование водителя</b> @{telegram}

📋 <b>Текущие данные:</b>
1. 👤 Имя: <code>{name}</code>
2. 🚗 Марка авто: <code>{car_model}</code>
3. 🎨 Цвет авто: <code>{car_color}</code>
4. 🔢 Гос. номер: <code>{car_number}</code>
5. 📞 Телефон: <code>{phone_number}</code>
6. 📱 Telegram: @{telegram}

Выберите номер поля для редактирования:"""
INVALID_FIELD_CHOICE = """❌ <b>Неверный выбор!</b>

Пожалуйста, выберите номер от 1 до 6"""
ENTER_NEW_VALUE = "✏️ Введите <b>новое значение</b> для {field}:"
ENTER_NEW_TELEGRAM = "📱 Введите <b>новый Telegram username</b> (без @):"
TELEGRAM_TAKEN = "❌ <b>Этот Telegram уже занят!</b>\nВведите другой username"
FIELD_UPDATED = "✅ <b>Данные успешно обновлены!</b>"
TELEGRAM_UPDATED = """✅ <b>Telegram успешно изменён!</b>

├ Было: @{old_telegram}
└ Стало: @{new_telegram}"""
UPDATE_ERROR = "❌ <b>Ошибка при обновлении:</b>\n<code>{error}</code>"

# Удаление водителя
ENTER_DELETE_TELEGRAM = """🗑️ <b>Удаление водителя</b>

Введите Telegram username водителя (без @):"""
DRIVER_DELETED = """✅ <b>Водитель успешно удалён!</b>

📋 <b>Данные удалённого водителя:</b>
├ 👤 Имя: {name}
├ 🚗 Авто: {car_model} ({car_color})
└ 📱 Telegram: @{telegram}"""
DELETE_ERROR = "❌ <b>Ошибка при удалении:</b>\n<code>{error}</code>"