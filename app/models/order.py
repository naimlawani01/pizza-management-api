from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

# Définition des différents statuts possibles d'une commande
class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# Modèle SQLAlchemy de la table "orders"
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default=OrderStatus.PENDING.value)  # Statut par défaut : pending
    items = Column(JSON, nullable=False)  # Liste des pizzas commandées (stockée en JSON)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Auto timestamp
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # Auto update timestamp

    user = relationship("User", back_populates="orders")
