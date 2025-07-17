import os
from dotenv import load_dotenv

load_dotenv()

class MainMenuTexts:
    @staticmethod
    def welcome(name: str) -> str:
        phones = os.getenv('DISPATCHER_PHONES', '').split(';')
        phones_text = '\n'.join(f'• {phone.strip()}' for phone in phones if phone.strip())
        return (
            f"Здравствуйте, {name}! 🚖\n"
            "Рады приветствовать вас в Кандринском Такси Форсаж\n\n"
            f"📞 Наши номера:\n{phones_text}"
        )

    PROFILE = "👤 Мой профиль"
    ORDER_TAXI = "🚖 Заказать такси"
    ABOUT = "ℹ️ О сервисе"
    BACK = "↩️ Назад"

class AboutServiceTexts:
    @staticmethod
    def description() -> str:
        phones = os.getenv('DISPATCHER_PHONES', '').split(';')
        phones_text = '\n'.join(f'• {phone.strip()}' for phone in phones if phone.strip())
        return (
            "🏎️ <b>Кандры Форсаж</b> - Быстро. Надежно. С драйвом!\n\n"
            "🔹 <b>Наши преимущества:</b>\n"
            "• Молниеносное прибытие по городу и между городами\n"
            "• Фиксированные цены - без скрытых платежей\n"
            "• Только опытные водители с безупречной репутацией\n"
            "• Современный и ухоженный автопарк\n\n"
            f"📞 <b>Заказ такси:</b>\n{phones_text}\n\n"
            "⏳ <b>Работаем:</b> 24/7 без выходных\n\n"
            "💵 <b>Оплата:</b> наличные / карта / СБП\n\n"
            "📍 <b>Зона работы:</b> Республика Башкортостан, ближайшие города и междугородние маршруты"
        )