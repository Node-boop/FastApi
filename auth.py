#! /usr/bin/python3

from fastapi import APIRouter,HTTPException,Response,status,Depends
from sqlalchemy.orm import Session
import models
from typing import List
from passlib.context import CryptContext
import schemas
from tokens import create_access_token
from database import Base,engine,SessionLocal,get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

router=APIRouter(
    prefix="/api/auth/login",
    tags=['Auth']
)




@router.post("/",status_code=status.HTTP_200_OK)
def main(user:OAuth2PasswordRequestForm=Depends(),db: Session=Depends(get_db)):
    user_query=db.query(models.User).filter(models.User.username== user.username).first()
    id = user_query.id
    print(f'[+] User id is',id)
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with those credentials not found")
    if not pwd_context.verify(user.password,user_query.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    access_token=create_access_token(data={"id":str(user_query.id)})
    print(user_query.id)
    print(access_token)
    return {"access_token":access_token,"token_type":"Bearer"}