from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from backend.database import SQLALCHEMY_DATABASE_URL
from backend.models import Base

def create_tables():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Tables created successfully")

if __name__ == "__main__":
    create_tables()