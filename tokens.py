#! /usr/bin/python3
from datetime import datetime,timedelta
from jose import JOSEError,jwt,JWTError
import schemas
from fastapi import HTTPException,Request,Depends,status
from fastapi.security.oauth2 import OAuth2PasswordBearer
import models
from sqlalchemy.orm import Session
from database import get_db
from config import settings

SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES=int(settings.EXPIRE_MINUTES)

outh_bearer=OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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

def check_admin(token: str=Depends(outh_bearer),db: Session=Depends(get_db)):
    admin=db.query(models.User).filter(models.User.isAdmin)
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Action Forbidden")
    elif admin:
        token_data=verify_access_token(token,HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token"))
    
    
    
    return token_data
