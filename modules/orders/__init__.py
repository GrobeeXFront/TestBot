from .handlers import router
from config import Config

async def setup():
    """Настройка модуля заказов"""
    Config.register_menu_item("orders", "🚖 Заказать такси")
    return router

__all__ = ['router', 'setup']