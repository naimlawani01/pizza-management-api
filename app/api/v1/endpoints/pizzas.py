from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.api.deps import get_current_user, get_db
from app.models.pizza import Pizza
from app.models.user import User
from app.schemas.pizza import Pizza as PizzaSchema
from app.schemas.pizza import PizzaCreate, PizzaUpdate

router = APIRouter()

@router.post("/", response_model=PizzaSchema)
def create_pizza(
    *,
    db: Session = Depends(get_db),
    pizza_in: PizzaCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new pizza.
    """
    pizza = Pizza(
        name=pizza_in.name,
        description=pizza_in.description,
        price=pizza_in.price,
        image_url=pizza_in.image_url,
        is_available=True
    )
    
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    return pizza

@router.get("/", response_model=List[PizzaSchema])
def read_pizzas(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve pizzas.
    """
    pizzas = db.query(Pizza).offset(skip).limit(limit).all()
    return pizzas

@router.get("/{pizza_id}", response_model=PizzaSchema)
def read_pizza(
    pizza_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get pizza by ID.
    """
    pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not pizza:
        raise HTTPException(
            status_code=404,
            detail="Pizza not found",
        )
    return pizza

@router.put("/{pizza_id}", response_model=PizzaSchema)
def update_pizza(
    *,
    db: Session = Depends(get_db),
    pizza_id: int,
    pizza_in: PizzaUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update pizza.
    """
    pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not pizza:
        raise HTTPException(
            status_code=404,
            detail="Pizza not found",
        )
    
    if pizza_in.name is not None:
        pizza.name = pizza_in.name
    if pizza_in.description is not None:
        pizza.description = pizza_in.description
    if pizza_in.price is not None:
        pizza.price = pizza_in.price
    if pizza_in.image_url is not None:
        pizza.image_url = pizza_in.image_url
    if pizza_in.is_available is not None:
        pizza.is_available = pizza_in.is_available
    
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    return pizza 