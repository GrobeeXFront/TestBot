from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Order(BaseModel):
    """Модель заказа такси"""
    id: Optional[int] = None
    client_id: int
    driver_id: Optional[int] = None
    pickup_location: str
    point_a: str
    point_b: str
    status: str = "pending"  # pending, accepted, in_progress, completed, cancelled
    created_at: Optional[datetime] = None
    estimated_arrival_time: Optional[int] = None
    actual_arrival_time: Optional[int] = None
    notes: Optional[str] = None