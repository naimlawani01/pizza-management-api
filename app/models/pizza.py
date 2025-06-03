from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ARRAY
from sqlalchemy.sql import func

from app.db.base_class import Base

class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    ingredients = Column(ARRAY(String), nullable=False)  # Liste des ingrédients
    price = Column(Float, nullable=False)
    image_url = Column(String)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 