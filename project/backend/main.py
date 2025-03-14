from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Order, OrderItem, Product
from schemas import OrderCreateSchema
from auth import get_current_user

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