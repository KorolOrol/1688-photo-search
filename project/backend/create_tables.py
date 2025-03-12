from database import engine, Base
from models import User, Order, Product, OrderItem

Base.metadata.create_all(bind=engine)