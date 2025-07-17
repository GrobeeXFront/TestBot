import aiomysql
from config import Config
from .models import Client

class ClientService:
    @staticmethod
    async def create_or_update(client: Client) -> bool:
        async with aiomysql.connect(**Config.DB_CONFIG) as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO clients 
                    (telegram_id, name, phone, location)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    phone = VALUES(phone),
                    location = VALUES(location)
                """, (
                    client.telegram_id,
                    client.name,
                    client.phone,
                    client.location
                ))
                await conn.commit()
                return True

    @staticmethod
    async def get_client(telegram_id: int) -> dict:
        async with aiomysql.connect(**Config.DB_CONFIG) as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "SELECT id, telegram_id, name, phone, location FROM clients WHERE telegram_id = %s",
                    (telegram_id,))
                return await cur.fetchone()

    @staticmethod
    async def get_client_by_id(client_id: int) -> dict:
        async with aiomysql.connect(**Config.DB_CONFIG) as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "SELECT id, telegram_id, name, phone, location FROM clients WHERE id = %s",
                    (client_id,))
                return await cur.fetchone()

    @staticmethod
    async def update_client(telegram_id: int, **fields):
        async with aiomysql.connect(**Config.DB_CONFIG) as conn:
            async with conn.cursor() as cur:
                set_clause = ", ".join([f"{k}=%s" for k in fields])
                await cur.execute(
                    f"UPDATE clients SET {set_clause} WHERE telegram_id=%s",
                    (*fields.values(), telegram_id)
                )
                await conn.commit()