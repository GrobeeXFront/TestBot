from aiomysql import Pool
from pydantic import BaseModel

class DriverService:
    def __init__(self, pool: Pool):
        self.pool = pool

    async def get_driver(self, driver_id: int) -> dict | None:
        """Получает данные водителя по ID"""
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "SELECT * FROM drivers WHERE id = %s", 
                        (driver_id,)
                    )
                    return await cursor.fetchone()
        except Exception as e:
            print(f"Error getting driver {driver_id}: {e}")
            return None