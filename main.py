# main.py (исправленная версия)
import asyncio
import logging
import sys
from pathlib import Path
from importlib import import_module
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config

print("Токен из .env:", Config.TOKEN)
print("Админы:", Config.ADMIN_IDS)

# Настройка путей
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(BASE_DIR / "bot.log")
    ]
)
logger = logging.getLogger(__name__)

class ModuleLoader:
    """Загрузчик модулей (исправленная версия)"""
    
    @staticmethod
    async def load_module(dp: Dispatcher, module_name: str) -> bool:
        try:
            module = import_module(f"modules.{module_name}")
            
            # Инициализация и подключение роутера
            if hasattr(module, 'setup'):
                router = await module.setup()  # Получаем роутер из setup()
                if router:
                    dp.include_router(router)
                    logger.info(f"Модуль '{module_name}' загружен")
                    return True
                
        except Exception as e:
            logger.error(f"Ошибка в модуле {module_name}: {str(e)}", exc_info=True)
        return False

    @staticmethod
    async def load_active_modules(dp: Dispatcher) -> int:
        """Загружает все активные модули из Config"""
        loaded = 0
        for module_name, is_active in Config.MODULES.items():
            if is_active and await ModuleLoader.load_module(dp, module_name):
                loaded += 1
        return loaded

async def setup_fallback(dp: Dispatcher):
    """Аварийный режим при проблемах"""
    fallback_router = Router()
    
    @fallback_router.message()
    async def fallback_handler(message):
        await message.answer("🔧 Бот на техническом обслуживании")
        
    dp.include_router(fallback_router)
    logger.warning("Активирован аварийный роутер")

async def main():
    """Точка входа"""
    logger.info("Запуск бота...")
    
    try:
        bot = Bot(
            token=Config.TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher(storage=MemoryStorage())
        
        # Загрузка модулей
        loaded = await ModuleLoader.load_active_modules(dp)
        if loaded == 0:
            await setup_fallback(dp)
            logger.error("Ни один модуль не загружен!")
        
        # Старт
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info(f"Бот запущен (модулей: {loaded})")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.critical(f"КРИТИЧЕСКАЯ ОШИБКА: {str(e)}", exc_info=True)
    finally:
        logger.info("Бот остановлен")
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Остановка по Ctrl+C")