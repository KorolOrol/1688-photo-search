from fastapi.testclient import TestClient
from jose import jwt
from datetime import timedelta
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..auth import app, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
from ..database import Base, get_db
from ..models import User as UserModel

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_module():
    Base.metadata.create_all(bind=engine)
@pytest.fixture(scope="session", autouse=True)
def setup_module():
    Base.metadata.create_all(bind=engine)

@pytest.fixture(autouse=True)
def setup_test_data():
    db = TestingSessionLocal()
    db.query(UserModel).delete()
    create_test_user(db, "user@example.com", "password")
    db.commit()
    db.close()
    db.commit()
    db.close()
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def create_test_user(db, username: str, password: str, disabled: bool = False):
    hashed_password = get_password_hash(password)
    user = UserModel(
        username=username,
        email=username,
        full_name=username,
        hashed_password=hashed_password,
        disabled=disabled,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(autouse=True)
def setup_test_data():
    db = TestingSessionLocal()
    db.query(UserModel).delete()
    create_test_user(db, "user@example.com", "password")
    db.commit()
    db.close()

def test_get_token():
    response = client.post(
        "/token",
        data={"username": "user@example.com", "password": "password"},
    )
    assert response.status_code == 200
    json_resp = response.json()
    assert "access_token" in json_resp
    assert json_resp["token_type"] == "bearer"

def test_get_token_invalid_credentials():
    response = client.post(
        "/token",
        data={"username": "user@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_read_users_me():
    token_resp = client.post(
        "/token",
        data={"username": "user@example.com", "password": "password"},
    )
    token = token_resp.json()["access_token"]
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "user@example.com"

def test_read_users_me_inactive_user():
    # Создаем неактивного пользователя
    db = next(override_get_db())
    create_test_user(db, "inactive@example.com", "password", disabled=True)

    token_resp = client.post(
        "/token",
        data={"username": "inactive@example.com", "password": "password"},
    )
    token = token_resp.json()["access_token"]
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