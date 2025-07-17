from .handlers import router
from config import Config

async def setup():
    """Настройка модуля admin"""
    Config.register_menu_item("admin", "👨‍💻 Админка")
    return router