from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class OrderItemBase(BaseModel):
    pizza_id: int
    quantity: int

class OrderBase(BaseModel):
    customer_id: int
    items: List[OrderItemBase]

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = None

class Order(OrderBase):
    id: int
    status: str
    total_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
