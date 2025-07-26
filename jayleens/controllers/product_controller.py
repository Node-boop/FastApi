#! /usr/bin/python3
from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from models import models
from middleware import schemas
from models.database import get_db


product_router = APIRouter()

@product_router.get("/api/products/list",status_code=status.HTTP_302_FOUND)
async def get_all_products():
    pass