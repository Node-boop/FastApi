#! /usr/bin/python3
from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
import models
from typing import List
from passlib.context import CryptContext
import schemas
from database import Base,engine,SessionLocal,get_db
import tokens
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

router=APIRouter(
    prefix="/api/v1/users",
    tags=['Users']
)



@router.get("/",response_model=List[schemas.UserOut])
async def main(db:Session=Depends(get_db),current_user: int =Depends(tokens.get_current_user)):
    users=db.query(models.User).all()
    if not users:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f' 404 No User Retrived')
    return users

@router.get("/{id}",response_model=schemas.UserOut)
def main(id:int,db:Session=Depends(get_db),current_user: int =Depends(tokens.get_current_user)):
    got_user=db.query(models.User).filter(models.User.id==current_user.id).first()
    if not got_user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id {id} not found')
    return got_user

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def main(user:schemas.User,db:Session=Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.username == user.username).first()
    user=models.User(username=user.username,email=user.email,password=user.password)
    hashed_pwassword=pwd_context.hash(user.password)
    user.password=hashed_pwassword
    if user_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="A user with the following credentials already exists")
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{id}")
def main(id:int,db:Session=Depends(get_db)):
    user_query=db.query(models.User).filter(models.User.id== id)
    new_user=user_query.first()
    if not new_user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id {id} not found')
    
    #if new_user.id!=current_user.id:
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="ACTION NOT ALOWWED")
    user_query.delete(synchronize_session=False)
    db.commit()
    return user_query.first()

@router.get("/{name}",response_model=schemas.UserOut)
def main(name:str,db:Session=Depends(get_db)):
    new_user=db.query(models.User).filter(models.User.name== name).first()

    if not new_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with name {name} not found")
    return new_user

@router.put("/{id}",response_model=schemas.UserOut)
def main(id:int,user:schemas.User,db:Session=Depends(get_db)):
    user_query=db.query(models.User).filter(models.User.id== id)
    new_user=user_query.first()
    if not new_user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id {id} not found')
    user_query.update({models.User.username:user.username,models.User.email:user.email,models.User.password:user.password})
    db.commit()
    return user_query.first()

@router.patch("/{id}",response_model=schemas.UserOut)
def main(id:int,user:schemas.EditUser,db:Session=Depends(get_db)):
    user_query=db.query(models.User).filter(models.User.id== id)
    new_user=user_query.first()
    if not new_user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id {id} not found')
    user_query.update({models.User.username:user.username,models.User.email:user.email,models.User.password:user.password})
    
    db.commit()
    return user_query.first()


