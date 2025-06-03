from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from .base import TimestampModel

class PizzaBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: Optional[str] = None
    is_available: bool = True

class PizzaCreate(PizzaBase):
    pass

class PizzaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None

class Pizza(PizzaBase, TimestampModel):
    id: int

    model_config = ConfigDict(from_attributes=True)
