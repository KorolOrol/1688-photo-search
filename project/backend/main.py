from fastapi import FastAPI, Depends, HTTPException
from pytz import timezone
from rsa import verify
from sqlalchemy.orm import Session
from .database import get_db
from .models import Order, OrderItem, Product
from .schemas import ImageRecognitionSchema, OrderCreateSchema
from .auth import get_current_user, get_password_hash, verify_password
from .models import User
from .schemas import UserCreateSchema, UserLoginSchema
from datetime import datetime, timedelta
import jwt
from fastapi import UploadFile, File, HTTPException
import shutil
import os
from .image_recognition import send_image_recognition_request
from .ml.parser import AliexpressParser

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
import base64

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать конкретные домены вместо "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user_id": new_user.id, "message": "User registered successfully"}

@app.post("/login")
def login_user(login_data: UserLoginSchema, db: Session = Depends(get_db)):
    print(login_data.email)
    user = db.query(User).filter(User.email == login_data.email).first()
    print(user.email)
    print(user.hashed_password)
    print(verify_password(login_data.password, user.hashed_password))
    if not user or not verify_password(login_data.password, user.hashed_password):
        print("error")
        raise HTTPException(status_code=400, detail="Invalid email or password")
    SECRET_KEY = "YOUR_SECRET_KEY"  # Replace with your actual secret key
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    token_data = {
        "sub": user.email,
        "iat": datetime.now(timezone('UTC')),
        "exp": datetime.now(timezone('UTC')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/products/search-by-photo")
async def search_by_photo(image: ImageRecognitionSchema):
    base64_string = image.image
    if not base64_string:
        raise HTTPException(status_code=400, detail="No image provided")
    print("Received image")
    image_recognition_url = "http://127.0.0.1:1234/v1/chat/completions"
    try:
        keywords = send_image_recognition_request(image.image, image_recognition_url)
        parser = AliexpressParser()
        products = parser.parse_products_cards(keywords)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"keywords": keywords, "products": products}