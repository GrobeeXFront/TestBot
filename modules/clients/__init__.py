from .handlers import router
from config import Config

async def setup(module_config=None):  # Добавляем параметр по умолчанию
    Config.register_menu_item("clients", "👤 Мой профиль")
    return router

__all__ = ['router', 'setup']