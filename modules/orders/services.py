from aiomysql import Pool
from pydantic import BaseModel

async def get_order(self, order_id: int) -> BaseModel | None:
    try:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
                return cursor.fetchone()
    except Exception as e:
        print(f"Error getting order {order_id}: {e}")
        return None

class OrderService:
    def __init__(self, pool: Pool):
        self.pool = pool

    async def create_order(self, client_id: int, point_a: str, point_b: str) -> BaseModel:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO orders (client_id, point_a, point_b, status) VALUES (%s, %s, %s, 'pending')",
                    (client_id, point_a, point_b)
                )
                await conn.commit()
                return await self.get_order(cursor.lastrowid)

    async def assign_driver(self, order_id: int, driver_id: int) -> BaseModel:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE orders SET driver_id = %s, status = 'assigned' WHERE id = %s",
                    (driver_id, order_id)
                )
                await conn.commit()
                return await self.get_order(order_id)

    async def get_order(self, order_id: int) -> BaseModel:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
                return cursor.fetchone()

    async def get_driver_details(self, driver_id: int) -> BaseModel:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM drivers WHERE id = %s", (driver_id,))
                return cursor.fetchone()
    
    async def reassign_order(self, order_id: int) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Находим нового водителя
                await cursor.execute(
                    "SELECT id FROM drivers WHERE is_available = 1 AND id NOT IN "
                    "(SELECT driver_id FROM orders WHERE id = %s) LIMIT 1",
                    (order_id,)
                )
                new_driver = await cursor.fetchone()
                
                if new_driver:
                    await self.assign_driver(order_id, new_driver[0])
                    return True
                return False