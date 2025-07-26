#! /usr/bin/python3
from jose import jwt,JOSEError,JWSError,JWTError
from middleware import schemas
from fastapi import HTTPException,status,Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from config import settings
from sqlalchemy.orm import Session
from models import models
from  datetime import datetime,timedelta

outh_bearer=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRE_MINUTES = int(settings.EXPIRE_MINUTES)
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


    return encoded_jwt

def verify_access_token(token:str,exception_raise):
    try:
        decoded_jwt=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id :str=decoded_jwt.get("id")
        print(f"My is is: {id} ")
        
        if id is None:
            raise exception_raise
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise exception_raise
    print(token_data)
    return token_data

def get_current_user(token: str = Depends(outh_bearer)):
    token_data=verify_access_token(token,HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Access Token"))


    return token_data