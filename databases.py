import aiomysql
from config import Config
import logging

logger = logging.getLogger(__name__)

class Database:
    _pool = None

    @classmethod
    async def get_pool(cls):
        if not cls._pool:
            try:
                cls._pool = await aiomysql.create_pool(
                    host=Config.DB_CONFIG['host'],
                    user=Config.DB_CONFIG['user'],
                    password=Config.DB_CONFIG['password'],
                    db=Config.DB_CONFIG['db'],
                    port=Config.DB_CONFIG['port'],
                    connect_timeout=Config.DB_CONFIG['connect_timeout'],
                    minsize=1,
                    maxsize=5
                )
                logger.info("✅ Пул MySQL подключений создан")
            except Exception as e:
                logger.critical(f"❌ Ошибка подключения к MySQL: {e}")
                raise
        return cls._pool

    @classmethod
    async def execute(cls, query, args=None):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, args)
                    await conn.commit()
                    return cur
                except Exception as e:
                    await conn.rollback()
                    logger.error(f"❌ Ошибка SQL: {e}")
                    raise