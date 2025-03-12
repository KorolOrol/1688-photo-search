from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from models import Base
from database import SQLALCHEMY_DATABASE_URL

def create_tables():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Tables created successfully")

if __name__ == "__main__":
    create_tables()