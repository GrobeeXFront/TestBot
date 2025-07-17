from datetime import datetime
from pydantic import BaseModel, validator

class Driver(BaseModel):
    name: str
    car_model: str
    car_color: str
    car_number: str
    phone: str
    telegram: str
    registration_date: datetime = datetime.now()
    is_active: bool = True

    @validator('phone')
    def phone_validator(cls, v):
        if not v.isdigit():
            raise ValueError("Номер телефона должен содержать только цифры")
        return v

    @validator('telegram')
    def telegram_validator(cls, v):
        return v.replace("@", "").strip()