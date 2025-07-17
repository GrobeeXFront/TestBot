import aiomysql
from datetime import datetime
from config import Config
from .models import Driver

class DriverService:
    @staticmethod
    async def create_driver(driver: Driver) -> int:
        async with aiomysql.connect(**Config.DB_CONFIG) as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO drivers 
                    (name, car_model, car_color, car_number, phone_number, telegram)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    driver.name,
                    driver.car_model,
                    driver.car_color,
                    driver.car_number,
                    driver.phone,
                    driver.telegram
                ))
                await conn.commit()
                return cur.lastrowid

    @staticmethod
    async def update_driver(driver_id: int, **fields):
        async with aiomysql.connect(**Config.DB_CONFIG) as conn:
            async with conn.cursor() as cur:
                set_clause = ", ".join([f"{k}=%s" for k in fields])
                await cur.execute(
                    f"UPDATE drivers SET {set_clause} WHERE id=%s",
                    (*fields.values(), driver_id)
                )
                await conn.commit()

    @staticmethod
    async def delete_driver(driver_id: int) -> bool:
        async with aiomysql.connect(**Config.DB_CONFIG) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "DELETE FROM drivers WHERE id=%s",
                    (driver_id,)
                )
                await conn.commit()
                return cur.rowcount > 0

    @staticmethod
    async def get_driver_by_telegram(telegram: str) -> dict:
        async with aiomysql.connect(**Config.DB_CONFIG) as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "SELECT * FROM drivers WHERE telegram=%s",
                    (telegram,)
                )
                return await cur.fetchone()

    @staticmethod
    async def is_telegram_exists(telegram: str, exclude_id: int = None) -> bool:
        async with aiomysql.connect(**Config.DB_CONFIG) as conn:
            async with conn.cursor() as cur:
                query = "SELECT 1 FROM drivers WHERE telegram = %s"
                params = [telegram]
                if exclude_id:
                    query += " AND id != %s"
                    params.append(exclude_id)
                await cur.execute(query, params)
                return bool(await cur.fetchone())