import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import User, Order, Product, OrderItem

DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope='module')
def engine():
    return create_engine(DATABASE_URL)

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_create_user(db_session):
    new_user = User(username="testuser", email="testuser@example.com", hashed_password="hashedpassword")
    db_session.add(new_user)
    db_session.commit()
    assert new_user.id is not None

def test_create_order(db_session):
    new_user = User(username="testuser2", email="testuser2@example.com", hashed_password="hashedpassword")
    db_session.add(new_user)
    db_session.commit()
    new_order = Order(user_id=new_user.id, total_price=100.0, status="new")
    db_session.add(new_order)
    db_session.commit()
    assert new_order.id is not None

def test_create_product(db_session):
    new_product = Product(name="Test Product", description="Test Description", price=10.0)
    db_session.add(new_product)
    db_session.commit()
    assert new_product.id is not None

def test_create_order_item(db_session):
    new_user = User(username="testuser3", email="testuser3@example.com", hashed_password="hashedpassword")
    db_session.add(new_user)
    db_session.commit()
    new_order = Order(user_id=new_user.id, total_price=200.0, status="new")
    db_session.add(new_order)
    db_session.commit()
    new_product = Product(name="Test Product 2", description="Test Description 2", price=20.0)
    db_session.add(new_product)
    db_session.commit()
    new_order_item = OrderItem(order_id=new_order.id, product_id=new_product.id, quantity=2)
    db_session.add(new_order_item)
    db_session.commit()
    assert new_order_item.id is not None