#! /usr/bin/python3
from pydantic import BaseModel,EmailStr
from models import User
from datetime import datetime
from typing import Optional

class EditUser(BaseModel):
    username:str
    password:str
    email:EmailStr




class User(BaseModel):
    username:str
    email: EmailStr
    password:str
    isAdmin: bool
        
class Post(BaseModel):
    title:str
    body:str
    
    

class UserOut(BaseModel):
    id: str
    username:str
    email: EmailStr
    isAdmin: bool
    joined: datetime
    
    class Config:
        from_attributes=True

class PostOut(BaseModel):
    id: int
    title:str
    body:str
    created_at: datetime
    owner_id: int
    class Config:
        from_attributes=True

class UserLogin(BaseModel):
    username:str
    password:str

class TokenData(BaseModel):
    id :str

class Token(BaseModel):
    access_token:str
    token_type:str
