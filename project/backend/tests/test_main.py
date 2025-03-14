import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.backend.main import app
from project.backend.database import Base, get_db
from project.backend.auth import get_current_user
from project.backend.models import Product

# Setup an in-memory SQLite database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Override get_current_user to return a dummy user for /orders/create tests
class DummyUser:
    id = 1
    email = "dummy@example.com"
    username = "dummy"

def override_get_current_user():
    return DummyUser()

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_register_user():
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["message"] == "User registered successfully"

def test_duplicate_register():
    payload = {
        "username": "testuser2",
        "email": "duplicate@example.com",
        "password": "pass"
    }
    response1 = client.post("/register", json=payload)
    assert response1.status_code == 200
    response2 = client.post("/register", json=payload)
    assert response2.status_code == 400
    data = response2.json()
    assert data["detail"] == "Email already registered"

def test_login_user():
    # First register a user for login
    reg_payload = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "loginpass"
    }
    reg_response = client.post("/register", json=reg_payload)
    assert reg_response.status_code == 200

    login_payload = {
        "email": "login@example.com",
        "password": "loginpass"
    }
    response = client.post("/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    login_payload = {
        "email": "nonexistent@example.com",
        "password": "wrongpass"
    }
    response = client.post("/login", json=login_payload)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid email or password"

def test_create_order(db):
    # For order creation, add a product to the testing DB.
    # Create a test product; adjust field names as required by your Product model.
    new_product = Product(name="Test Product", price=10.0)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    order_payload = {
        "items": [
            {"product_id": new_product.id, "quantity": 2}
        ]
    }
    response = client.post("/orders/create", json=order_payload)
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert data["status"] == "created"

def test_create_order_product_not_found():
    # Attempt to create an order with a non-existent product id.
    order_payload = {
        "items": [
            {"product_id": 9999, "quantity": 1}
        ]
    }
    response = client.post("/orders/create", json=order_payload)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"