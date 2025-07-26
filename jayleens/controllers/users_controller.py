#! /usr/bin/python3

from fastapi import APIRouter,HTTPException,Response,status,Depends
from sqlalchemy.orm import Session
import models
from typing import List
from passlib.context import CryptContext
from middleware import schemas
from middleware.tokens import get_current_user
from models.database import Base,engine,SessionLocal,get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models import models

from middleware import schemas
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

router=APIRouter(
    
    tags=['users']

)

@router.get("/api/v1/users",response_model=List[schemas.UserOut],status_code=status.HTTP_302_FOUND)
async def get_users(db:Session = Depends(get_db),current_user = Depends(get_current_user) ):
    users=db.query(models.User).all()
    if not users:
        print("[-]         No Users Found")
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f' 404 No User Retrived')
    return users


@router.post("/api/auth/register",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def register_user(user: schemas.User, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == user.email).first()

    if user_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="A user with the following credentials already exists")
    
    user=models.User(full_name=user.full_name,email=user.email,phone=user.phone,password=user.password)
    hashed_pwassword=pwd_context.hash(user.password)
    user.password=hashed_pwassword
    db.add(user)
    db.commit()
    db.refresh(user)


    return user

    
