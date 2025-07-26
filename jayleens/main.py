#! /usr/bin/python3

from fastapi import FastAPI
from models.database import Base,get_db,engine,SessionLocal
from controllers import users_controller
from models import models
from controllers import users_controller
from controllers import cart_controller
import auth
app = FastAPI()


try:
    models.Base.metadata.create_all(bind=engine)
    print("[+] Database Connection Success!!")

except Exception as e:
    print("Error " ,e)

app.include_router(users_controller.router)
app.include_router(cart_controller.cart_router)
app.include_router(auth.router)

