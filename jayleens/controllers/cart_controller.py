#! /usr/bin/python3
from fastapi import APIRouter,Depends,HTTPException,status
from middleware.tokens import get_current_user
from models.models import User
from middleware import schemas
from models.database import get_db
from sqlalchemy.orm import Session
cart_router = APIRouter()

@cart_router.post("/api/v1/cart/add",status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(cart:schemas.Cart, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    user_query = db.query(User).filter(User._id == current_user.id)
    new_user = user_query.first()
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Login to add items to cart")
    #user_query.cart_data = dict(cart.items)
    user_query.update({User.cart_data: cart.items})
    db.commit()
    db.refresh(new_user)
    return new_user
@cart_router.delete("/api/v1/cart/remove")
async def remove_product_from_cart():
    pass

@cart_router.put("/api/v1/cart/update")
async def update_product_quantity():
    pass
