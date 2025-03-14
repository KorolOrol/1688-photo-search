from fastapi.testclient import TestClient
from jose import jwt
from datetime import timedelta
from ..auth import app, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db, get_password_hash

client = TestClient(app)

def test_get_token():
    response = client.post(
        "/token",
        data={"username": "user@example.com", "password": "password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_get_token_invalid_credentials():
    response = client.post(
        "/token",
        data={"username": "user@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_read_users_me():
    response = client.post(
        "/token",
        data={"username": "user@example.com", "password": "password"},
    )
    token = response.json()["access_token"]
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "user@example.com"

def test_read_users_me_inactive_user():
    fake_users_db["inactive@example.com"] = {
        "username": "inactive@example.com",
        "full_name": "Inactive User",
        "email": "inactive@example.com",
        "hashed_password": get_password_hash("password"),
        "disabled": True,
    }
    response = client.post(
        "/token",
        data={"username": "inactive@example.com", "password": "password"},
    )
    token = response.json()["access_token"]
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Inactive user"}

def test_create_access_token():
    data = {"sub": "user@example.com"}
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == "user@example.com"