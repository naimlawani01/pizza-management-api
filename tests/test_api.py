from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.api.deps import get_db, get_current_user
from datetime import datetime, UTC
from app.models.order import OrderStatus
from app.models.user import User

client = TestClient(app)

# Mock de la session de base de données
mock_db = MagicMock()

# Mock de l'utilisateur authentifié
mock_user = User(
    id=1,
    email="test@example.com",
    username="testuser",
    first_name="Test",
    last_name="User",
    is_active=True,
    is_superuser=True
)

# Override des dépendances
app.dependency_overrides[get_db] = lambda: mock_db
app.dependency_overrides[get_current_user] = lambda: mock_user

def test_get_pizzas():
    """Test de l'endpoint GET /pizzas"""
    now = datetime.now(UTC)
    mock_response = [
        {
            "id": 1,
            "name": "Margherita",
            "description": "Sauce tomate, mozzarella, basilic",
            "price": 10.99,
            "image_url": "https://example.com/margherita.jpg",
            "is_available": True,
            "created_at": now,
            "updated_at": now
        }
    ]
    
    # Mock de la requête à la base de données
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_response
    
    response = client.get("/api/v1/pizzas")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Margherita"
    assert response.json()[0]["price"] == 10.99
    
    # Vérification que la requête a été faite avec les bons paramètres
    mock_db.query.assert_called_once()
    mock_db.query.return_value.offset.assert_called_once_with(0)
    mock_db.query.return_value.offset.return_value.limit.assert_called_once_with(100)

def test_get_pizza_by_id():
    """Test de l'endpoint GET /pizzas/{pizza_id}"""
    now = datetime.now(UTC)
    mock_pizza = {
        "id": 1,
        "name": "Margherita",
        "description": "Sauce tomate, mozzarella, basilic",
        "price": 10.99,
        "image_url": "https://example.com/margherita.jpg",
        "is_available": True,
        "created_at": now,
        "updated_at": now
    }
    
    # Mock de la requête à la base de données
    mock_db.query.return_value.filter.return_value.first.return_value = mock_pizza
    
    response = client.get("/api/v1/pizzas/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Margherita"
    assert response.json()["price"] == 10.99

def test_get_orders():
    """Test de l'endpoint GET /orders"""
    now = datetime.now(UTC)
    mock_orders = [
        {
            "id": 1,
            "user_id": 1,
            "status": OrderStatus.PENDING.value,
            "items": [
                {
                    "pizza_id": 1,
                    "pizza_name": "Margherita",
                    "quantity": 2,
                    "unit_price": 10.99,
                    "subtotal": 21.98
                }
            ],
            "total_price": 21.98,
            "created_at": now,
            "updated_at": now
        }
    ]
    
    # Mock de la requête à la base de données
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_orders
    
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == OrderStatus.PENDING.value
    assert response.json()[0]["total_price"] == 21.98

def test_get_order_by_id():
    """Test de l'endpoint GET /orders/{order_id}"""
    now = datetime.now(UTC)
    mock_order = {
        "id": 1,
        "user_id": 1,
        "status": OrderStatus.PENDING.value,
        "items": [
            {
                "pizza_id": 1,
                "pizza_name": "Margherita",
                "quantity": 2,
                "unit_price": 10.99,
                "subtotal": 21.98
            }
        ],
        "total_price": 21.98,
        "created_at": now,
        "updated_at": now
    }
    
    # Mock de la requête à la base de données
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order
    
    response = client.get("/api/v1/orders/1")
    assert response.status_code == 200
    assert response.json()["status"] == OrderStatus.PENDING.value
    assert response.json()["total_price"] == 21.98 