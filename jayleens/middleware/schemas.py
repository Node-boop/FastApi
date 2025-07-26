#! /usr/bin/python3
from pydantic import BaseModel,EmailStr
from models.models import User
from datetime import datetime
from typing import Optional

class User(BaseModel):
    full_name:str
    email: EmailStr
    phone:str
    password:str
   
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:str
    full_name:str
    email: EmailStr
    phone:str
    joined:datetime
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    id:str


class Cart(BaseModel):
    _id:str
    items:dict

class Login(BaseModel):
    email:EmailStr
    password:str


class Product(BaseModel):
    name:str
    category:str
    sub_category:str
    price:float
    color:str
    sku:str