from pydantic import BaseModel
from typing import List

class OrderItemCreateSchema(BaseModel):
    product_id: int
    quantity: int

class OrderCreateSchema(BaseModel):
    items: List[OrderItemCreateSchema]

class UserCreateSchema(BaseModel):
    email: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class ImageRecognitionSchema(BaseModel):
    image: str