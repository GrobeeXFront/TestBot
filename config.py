from pathlib import Path
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv(Path(__file__).parent / '.env')

class Config:
    """Конфигурация бота Кандры Форсаж"""
    
    # Безопасность (берётся из .env)
    TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS: List[int] = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
    
    # Чат-группы (берётся из .env)
    CHATS: Dict[str, int] = {
        'drivers': int(os.getenv("DRIVERS_CHAT", "0")),
        'logs': int(os.getenv("LOGS_CHAT", "0")),
        'support': int(os.getenv("SUPPORT_CHAT", "0"))
    }
    
    # Номера диспетчеров
    DISPATCHER_PHONES: List[str] = [
        phone.strip() 
        for phone in os.getenv("DISPATCHER_PHONES", "").split(",") 
        if phone.strip()
    ]
    
    # Пути
    BASE_DIR: Path = Path(__file__).parent
    DB_PATH: Path = BASE_DIR / "database" / "kandry_taxi.db"
    
    # Настройки MySQL
    DB_CONFIG: Dict[str, Optional[str | int]] = {
        'host': os.getenv("DB_HOST"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASS"),
        'db': os.getenv("DB_NAME"),
        'port': 3306,
        'connect_timeout': 10
    }
    
    # Модули
    MODULES: Dict[str, bool] = {
        "main_menu": True,
        "clients": True,
        "orders": False,
        "admin": False,
        "errors": False
    }

    # Меню
    _MENU_ITEMS: Dict[str, str] = {
        "admin": "👨‍💻 Админка",
        "orders": "🚖 Заказы"
    }

    @classmethod
    def register_menu_item(cls, module_name: str, button_text: str):
        """Регистрация пункта меню для модуля"""
        if module_name not in cls.MODULES:
            raise ValueError(f"Модуль {module_name} не зарегистрирован в конфигурации!")
        cls._MENU_ITEMS[module_name] = button_text

    @classmethod
    def get_menu_items(cls) -> List[str]:
        """Получение активных пунктов меню"""
        return [text for module, text in cls._MENU_ITEMS.items() 
               if cls.MODULES.get(module, False)]

    @classmethod
    def validate(cls):
        """Проверка обязательных настроек"""
        errors = []
        
        if not cls.TOKEN:
            errors.append("Токен бота (BOT_TOKEN) не указан в .env!")
        
        if not cls.ADMIN_IDS:
            errors.append("ID администраторов (ADMIN_IDS) не указаны в .env!")
        
        if not cls.DISPATCHER_PHONES:
            errors.append("Номера диспетчеров (DISPATCHER_PHONES) не указаны в .env!")
        
        # Проверка настроек БД
        if not all(cls.DB_CONFIG.values()):
            errors.append("Не все настройки базы данных указаны в .env!")
        
        if errors:
            error_msg = "\n".join(f"❌ {error}" for error in errors)
            raise ValueError(f"Ошибки конфигурации:\n{error_msg}")

# Инициализация и валидация конфигурации
try:
    Config.validate()
except ValueError as e:
    print(e)
    exit(1)

config = Config()