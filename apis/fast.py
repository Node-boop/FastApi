#! /usr/bin/python3
from fastapi import Depends, FastAPI,status,HTTPException
import database
from typing import List,Optional
from sqlalchemy.orm import Session
import models
from pydantic import BaseModel
from database import Base,engine,SessionLocal
import schemas
models.Base.metadata.create_all(bind=engine)

app=FastAPI()



def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()




@app.get("/api/v1/user",response_model=List[schemas.User])
async def main(db:Session=Depends(get_db)):
    teachers=db.query(models.User).all()
    if not teachers:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f'NOT FOUND')
    return teachers
@app.post("/api/v1/user",status_code=status.HTTP_201_CREATED,response_model=schemas.User)
def main(user:schemas.User,db:Session=Depends(get_db)):
    user=models.User(username=user.username,email=user.email,password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    if user.username is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Username of email already exist")
    return user

@app.get("/api/v1/teacher/{id}",response_model=schemas.User)
def main(id:int,db:Session=Depends(get_db)):
    got_teachers=db.query(models.User).filter(models.User.id== id).first()
    if not got_teachers:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f'Teacher with id {id} not found')
    return got_teachers
@app.put("/api/v1/teacher/{id}")
def main(id:int,updated_teacher:schemas.User,db:Session=Depends(get_db)):
    teacher_query=db.query(models.User).filter(models.User.id== id)
    new_teacher=teacher_query.first()
    if not new_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"teacher with id {id} not found")
    
    teacher_query.update(updated_teacher.dict(),synchronize_session=False)
    db.commit()
    db.refresh(new_teacher)
    return teacher_query.first()

@app.delete("/api/v1/teacher/{id}")
def main(id:int,db:Session=Depends(get_db)):
    teacher_query=db.query(models.User).filter(models.User.id== id)
    new_teacher=teacher_query.first()
    if not new_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"teacher with id {id} not found")
    teacher_query.delete(synchronize_session=False)
    db.commit()
    return teacher_query.first()

@app.get("/api/v1/teachers/{name}")
def main(name:str,db:Session=Depends(get_db)):
    new_teacher=db.query(models.User).filter(models.User.name== name).first()

    if not new_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with name {name} not found")
    return new_teacher