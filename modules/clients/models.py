from datetime import datetime
from pydantic import BaseModel, validator

class Client(BaseModel):
    """
    🧑‍💼 Модель клиента KandryTaxi
    """
    telegram_id: int
    name: str
    phone: str
    location: str
    registration_date: datetime = datetime.now()

    @validator('phone')
    def phone_validator(cls, v):
        """🔢 Валидация номера телефона"""
        if not v.isdigit():
            raise ValueError("🚫 Номер должен содержать только цифры")
        if len(v) < 10:
            raise ValueError("🚫 Номер слишком короткий")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "telegram_id": 123456789,
                "name": "Иван Иванов",
                "phone": "79123456789",
                "location": "г. Казань"
            }
        }