from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, customers, pizzas, orders

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(pizzas.router, prefix="/pizzas", tags=["pizzas"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"]) 