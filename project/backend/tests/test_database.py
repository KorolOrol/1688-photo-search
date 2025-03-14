import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from ..database import Base, SQLALCHEMY_DATABASE_URL
from sqlalchemy import Column, Integer, String

# Create a new engine and session for testing
engine_test = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# Create a new base for testing
BaseTest = declarative_base()

# Define a sample model for testing
class TestModel(Base):
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Dependency to get DB session for testing
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def setup_database():
    # Create the test database
    Base.metadata.create_all(bind=engine_test)
    yield
    # Drop the test database
    Base.metadata.drop_all(bind=engine_test)

@pytest.fixture(scope="function")
def db_session(setup_database):
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_get_db(db_session):
    db = next(get_test_db())
    assert db is not None
    assert db.bind.url == engine_test.url

def test_add_record(db_session):
    new_record = TestModel(name="Test Name")
    db_session.add(new_record)
    db_session.commit()
    db_session.refresh(new_record)
    assert new_record.id is not None
    assert new_record.name == "Test Name"

def test_read_record(db_session):
    new_record = TestModel(name="Test Name")
    db_session.add(new_record)
    db_session.commit()
    db_session.refresh(new_record)
    record = db_session.query(TestModel).filter_by(name="Test Name").first()
    assert record is not None
    assert record.name == "Test Name"

def test_delete_record(db_session):
    new_record = TestModel(name="Test Name")
    db_session.add(new_record)
    db_session.commit()
    db_session.refresh(new_record)
    db_session.delete(new_record)
    db_session.commit()
    record = db_session.query(TestModel).filter_by(name="Test Name").first()
    assert record is None

