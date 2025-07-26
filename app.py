#! /usr/bin/python3
from fastapi import FastAPI,status,Depends,HTTPException
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
import models
from typing import List
from passlib.context import CryptContext
import schemas
from database import Base,engine,SessionLocal
import users
import posts
import auth
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
app=FastAPI()

#models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def start_up_db_client():
    try:

        app.mongodb_client = AsyncIOMotorClient("mongodb://localhost:27017")
        app.mongodb = app.mongodb_client['jayleens']
        print(f"[+] Connection to database success")
    except EOFError as e:
        print(e)

@app.on_event('shutdown')
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)