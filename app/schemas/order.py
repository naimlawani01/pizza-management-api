from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from .base import TimestampModel
from .user import User
from .customer import Customer
from .pizza import Pizza

class OrderItemBase(BaseModel):
    pizza_id: int
    quantity: int
    unit_price: float
    subtotal: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    pizza: Pizza

    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    customer_id: int
    pizza_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = None

class Order(OrderBase):
    id: int
    status: str
    total_price: float

    class Config:
        from_attributes = True 