# Import the base class first
from app.db.base_class import Base

# Import models in the correct order
from app.models.user import User
from app.models.customer import Customer
from app.models.pizza import Pizza
from app.models.order import Order

# This is needed for Alembic to detect all models
__all__ = ["Base", "User", "Customer", "Pizza", "Order"] 