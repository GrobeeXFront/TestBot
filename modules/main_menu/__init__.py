from .handlers import router
from config import Config

async def setup():
    """Настройка модуля главного меню"""
    Config.register_menu_item("main_menu", "🏠 Главное меню")
    return router

__all__ = ['setup']