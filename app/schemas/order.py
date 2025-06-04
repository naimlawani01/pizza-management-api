from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class OrderItemBase(BaseModel):
    pizza_id: int
    quantity: int

class OrderBase(BaseModel):
    user_id: int
    items: List[OrderItemBase]

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = None

class OrderModify(BaseModel):
    items: List[OrderItemBase]

class OrderItemResponse(BaseModel):
    pizza_id: int
    pizza_name: str
    quantity: int
    unit_price: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)

class Order(OrderBase):
    id: int
    status: str
    total_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)
