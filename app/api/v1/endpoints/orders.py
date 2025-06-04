from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api import deps
from app.api.deps import get_current_user, get_db
from app.models.order import Order as OrderModel
from app.models.pizza import Pizza as PizzaModel
from app.models.user import User
from app.schemas.order import Order as OrderSchema
from app.schemas.order import OrderCreate, OrderUpdate, OrderModify
from app.models.order import OrderStatus

router = APIRouter()

# Création d'une commande
@router.post("/", response_model=OrderSchema)
def create_order(
    *,
    db: Session = Depends(get_db),
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Créer une nouvelle commande avec plusieurs pizzas.
    """
    # Vérifie si le user existe
    user = db.query(User).filter(User.id == order_in.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_price = 0
    items_payload = []

    for item in order_in.items:
        pizza = db.query(PizzaModel).filter(PizzaModel.id == item.pizza_id).first()
        if not pizza:
            raise HTTPException(status_code=404, detail=f"Pizza with id {item.pizza_id} not found")
        if not pizza.is_available:
            raise HTTPException(status_code=400, detail=f"Pizza {pizza.name} is not available")

        subtotal = pizza.price * item.quantity
        total_price += subtotal

        items_payload.append({
            "pizza_id": item.pizza_id,
            "pizza_name": pizza.name,
            "quantity": item.quantity,
            "unit_price": pizza.price,
            "subtotal": subtotal
        })

    order = OrderModel(
        user_id=order_in.user_id,
        status=OrderStatus.PENDING.value,
        items=items_payload,
        total_price=total_price
    )

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


# Lecture de toutes les commandes
@router.get("/", response_model=List[OrderSchema])
def read_orders(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Récupérer la liste de toutes les commandes.
    """
    orders = db.query(OrderModel).offset(skip).limit(limit).all()
    return orders


# Lecture d'une commande par ID
@router.get("/{order_id}", response_model=OrderSchema)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Récupérer une commande par son ID.
    """
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# Modification du statut de la commande
@router.put("/{order_id}", response_model=OrderSchema)
def update_order_status(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    order_in: OrderUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Mettre à jour le statut d'une commande.
    """
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order_in.status is not None:
        if order_in.status not in [status.value for status in OrderStatus]:
            raise HTTPException(status_code=400, detail="Invalid status value")
        order.status = order_in.status

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


# Suppression de la commande (annulation autorisée uniquement dans les 5 premières minutes)
@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Supprimer une commande (uniquement si elle a moins de 5 minutes).
    """
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    now = datetime.utcnow()
    created_at = order.created_at.replace(tzinfo=None)
    if now - created_at > timedelta(minutes=5):
        raise HTTPException(
            status_code=400,
            detail="Order can no longer be cancelled after 5 minutes."
        )

    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}


# Modification des items de la commande (possible uniquement si status == pending)
@router.put("/{order_id}/modify", response_model=OrderSchema)
def modify_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    order_in: OrderModify,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Modifier les items d'une commande uniquement si son statut est encore 'pending'.
    """
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != OrderStatus.PENDING.value:
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be modified."
        )

    total_price = 0
    items_payload = []

    for item in order_in.items:
        pizza = db.query(PizzaModel).filter(PizzaModel.id == item.pizza_id).first()
        if not pizza:
            raise HTTPException(status_code=404, detail=f"Pizza with id {item.pizza_id} not found")
        if not pizza.is_available:
            raise HTTPException(status_code=400, detail=f"Pizza {pizza.name} is not available")

        subtotal = pizza.price * item.quantity
        total_price += subtotal

        items_payload.append({
            "pizza_id": item.pizza_id,
            "pizza_name": pizza.name,
            "quantity": item.quantity,
            "unit_price": pizza.price,
            "subtotal": subtotal
        })

    order.items = items_payload
    order.total_price = total_price

    db.add(order)
    db.commit()
    db.refresh(order)
    return order
