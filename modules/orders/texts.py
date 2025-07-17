# modules/orders/texts.py
class OrderTexts:
    # Кнопки
    ORDER_BUTTON = "🚖 Заказать такси"
    EDIT_POINT_A_BTN = "✏️ Изменить Точку А"
    EDIT_POINT_B_BTN = "✏️ Изменить Точку Б"
    CONFIRM_ORDER_BTN = "✅ Подтвердить заказ"
    CANCEL_ORDER_BTN = "❌ Отменить заказ"
    CANCEL_BTN = "❌ Отмена"
    ACCEPT_ORDER_BTN = "✅ Принять заказ"
    SKIP_ORDER_BTN = "❌ Пропустить заказ"

    # Сообщения
    PROFILE_REQUIRED = "❌ Сначала необходимо создать профиль"
    
    POINT_A_PROMPT = (
        "📍 <b>Введите адрес отправления (Точка А):</b>\n\n"
        "<i>Пример: г. Кандры, ул. Ленина 15</i>\n\n"
        "Или нажмите «{cancel_btn}» чтобы прервать"
    )
    
    POINT_B_PROMPT = (
        "📍 <b>Введите адрес назначения (Точка Б):</b>\n\n"
        "<i>Пример: г. Кандры, ул. Мира 42</i>\n\n"
        "Или нажмите «{cancel_btn}» чтобы прервать"
    )
    
    ORDER_CONFIRMATION = (
        "🚖 <b>Проверьте детали заказа:</b>\n\n"
        "📍 Город: {pickup_location}\n"
        "🅰️ Откуда: {point_a}\n"
        "🅱️ Куда: {point_b}\n\n"
        "{confirm_btn} или изменить адреса:"
    )
    
    ORDER_ACCEPTED = "✅ <b>Заказ принят!</b>\n\nОжидайте подтверждения водителя"
    
    DRIVER_ASSIGNED = (
        "🚕 Водитель принял ваш заказ #{order_id}!\n\n"
        "👨‍✈️ <b>Информация о водителе:</b>\n"
        "   └ <b>Имя:</b> {driver_name}\n"
        "   └ <b>Авто:</b> {car_color} {car_model}\n"
        "   └ <b>Гос. номер:</b> <code>{car_number}</code>\n\n"
        "⏳ Скоро приедет по указанному адресу!\n\n"
        "📞 Для связи: @{driver_username}"
    )
    
    NEW_ORDER_NOTIFICATION = (
        "🚖 <b>НОВЫЙ ЗАКАЗ</b>\n\n"
        "👤 Клиент: {client_name}\n"
        "📞 Телефон: {client_phone}\n"
        "📱 Telegram: @{client_username}\n\n"
        "📍 Город: {pickup_location}\n"
        "🅰️ Откуда: {point_a}\n"
        "🅱️ Куда: {point_b}\n\n"
        "⏳ Ожидает подтверждения"
    )
    
    ORDER_ERROR = (
        "❌ <b>Ошибка создания заказа</b>\n"
        "Попробуйте позже или обратитесь в поддержку\n\n"
        "Ошибка: {error}"
    )
    
    SERVICE_UNAVAILABLE = "⚠️ Сервис временно недоступен"
    ORDER_SKIPPED = "❌ Заказ пропущен"
    ORDER_ACCEPTED_BY_DRIVER = "✅ Принял: @{username}"