#! /usr/bin/python3
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException,APIRouter
import models
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
import schemas
from tokens import create_access_token
from database import Base,engine,SessionLocal,get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

router=APIRouter(
    prefix='/admin'
    
)
@router.post("/",status_code=status.HTTP_200_OK)
def main(user:OAuth2PasswordRequestForm=Depends(),db: Session=Depends(get_db)):
    user_query=db.query(models.User).filter(models.User.username== user.username).first()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    if not pwd_context.verify(user.password,user_query.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    access_token=create_access_token(data={"sub":user_query.isAdmin})
    return {"access_token":access_token,"token_type":"Bearer"}