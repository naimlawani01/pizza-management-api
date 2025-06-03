from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.api.deps import get_current_user, get_db
from app.models.order import Order as OrderModel
from app.models.pizza import Pizza as PizzaModel
from app.models.customer import Customer
from app.models.user import User
from app.schemas.order import Order as OrderSchema
from app.schemas.order import OrderCreate, OrderUpdate

router = APIRouter()

@router.post("/", response_model=OrderSchema)
def create_order(
    *,
    db: Session = Depends(get_db),
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new order.
    """
    # Vérifier que le client existe
    customer = db.query(Customer).filter(Customer.id == order_in.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    # Calcul du total et vérification des pizzas
    total_price = 0
    items_payload = []

    for item in order_in.items:
        pizza = db.query(PizzaModel).filter(PizzaModel.id == item.pizza_id).first()
        if not pizza:
            raise HTTPException(status_code=404, detail=f"Pizza with id {item.pizza_id} not found")
        if not pizza.is_available:
            raise HTTPException(status_code=400, detail=f"Pizza with id {item.pizza_id} is not available")
        subtotal = pizza.price * item.quantity
        total_price += subtotal
        items_payload.append({
            "pizza_id": item.pizza_id,
            "quantity": item.quantity,
            "unit_price": pizza.price,
            "subtotal": subtotal
        })

    order = OrderModel(
        customer_id=order_in.customer_id,
        status="pending",
        items=items_payload,
        total_price=total_price
    )

    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=List[OrderSchema])
def read_orders(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve orders.
    """
    orders = db.query(OrderModel).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=OrderSchema)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get order by ID.
    """
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )
    return order

@router.put("/{order_id}", response_model=OrderSchema)
def update_order_status(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    order_in: OrderUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update order status.
    """
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    if order_in.status is not None:
        order.status = order_in.status

    db.add(order)
    db.commit()
    db.refresh(order)
    return order
