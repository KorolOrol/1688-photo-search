from fastapi import FastAPI, Depends, HTTPException
from pytz import timezone
from sqlalchemy.orm import Session
from database import get_db
from models import Order, OrderItem, Product
from schemas import OrderCreateSchema
from auth import get_current_user, hash_password
from models import User
from schemas import UserCreateSchema
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

app = FastAPI()

@app.post("/orders/create")
def create_order(order: OrderCreateSchema, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_order = Order(user_id=user.id, status='new')
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        order_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(order_item)

    db.commit()
    return {"order_id": new_order.id, "status": "created"}

@app.post("/register")
def register_user(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user_id": new_user.id, "message": "User registered successfully"}

class UserLoginSchema(BaseModel):
    email: str
    password: str

@app.post("/login")
def login_user(login_data: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or user.hashed_password != hash_password(login_data.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    SECRET_KEY = "YOUR_SECRET_KEY"  # Replace with your actual secret key
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    token_data = {
        "sub": user.email,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

