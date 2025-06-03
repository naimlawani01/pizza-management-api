from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from .base import TimestampModel

class IngredientBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True
    stock_quantity: int = 0

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    stock_quantity: Optional[int] = None

class Ingredient(IngredientBase, TimestampModel):
    id: int

    model_config = ConfigDict(from_attributes=True)

class PizzaBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: Optional[str] = None
    is_available: bool = True

class PizzaCreate(PizzaBase):
    ingredient_ids: List[int]

class PizzaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    ingredient_ids: Optional[List[int]] = None

class Pizza(PizzaBase, TimestampModel):
    id: int
    ingredients: List[Ingredient]

    model_config = ConfigDict(from_attributes=True) 