from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.customer import Customer
from app.models.user import User
from app.schemas.customer import Customer as CustomerSchema
from app.schemas.customer import CustomerCreate

router = APIRouter()

@router.post("/", response_model=CustomerSchema)
def create_customer(
    *,
    db: Session = Depends(get_db),
    customer_in: CustomerCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new customer.
    """
    # Vérifier si le client existe déjà
    customer = db.query(Customer).filter(Customer.email == customer_in.email).first()
    if customer:
        raise HTTPException(
            status_code=400,
            detail="A customer with this email already exists.",
        )
    
    # Créer le nouveau client
    customer = Customer(
        email=customer_in.email,
        first_name=customer_in.first_name,
        last_name=customer_in.last_name,
        phone=customer_in.phone,
        address=customer_in.address
    )
    
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@router.get("/", response_model=List[CustomerSchema])
def read_customers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve customers.
    """
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model=CustomerSchema)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get customer by ID.
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )
    return customer 