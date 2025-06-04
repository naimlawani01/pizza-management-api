from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

# Modèle de chaque item dans la commande (payload de création reçu depuis le frontend)
class OrderItemBase(BaseModel):
    pizza_id: int
    quantity: int

# Payload général de création d'une commande
class OrderBase(BaseModel):
    user_id: int
    items: List[OrderItemBase]

class OrderCreate(OrderBase):
    pass

# Payload pour mise à jour du statut uniquement
class OrderUpdate(BaseModel):
    status: Optional[str] = None

# Payload de modification d'une commande (changement des items)
class OrderModify(BaseModel):
    items: List[OrderItemBase]

# Payload enrichi renvoyé dans les réponses API
class OrderItemResponse(BaseModel):
    pizza_id: int
    pizza_name: str
    quantity: int
    unit_price: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)

# Schéma de réponse complet d'une commande
class Order(OrderBase):
    id: int
    status: str
    total_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)
