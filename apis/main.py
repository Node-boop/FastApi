#! /usr/bin/python3
from fastapi import FastAPI,status
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_sqlalchemy import SQLAlchemy
import pymysql
from pydantic import BaseModel
from pymysql.cursors import DictCursor
from database import Base,engine
from schemas import Post
from models import Teacher
import models
app=FastAPI()

def PostTeacher(BaseModel):
    name:str
    age:int
    height:str

models.Base.metadata.create_all(bind=engine)


try:
    db=pymysql.connect(host='localhost',user='root',database='fastapi',password='king')
    cursor=db.cursor(pymysql.cursors.DictCursor)
    print('connected')
except Exception as error:
    print(error)
    exit()

@app.post("/api/v1/add-teacher")
def post(post: PostTeacher):
    cursor.execute("insert into teachers(name,age,height) values(%s,%s,%s)",(post.name,post.age,post.height))
    db.commit()
    teacher=cursor.fetchone()
    return teacher



@app.get("/api/v1/students")
async def main():
    cursor.execute("select * from students")
    data=cursor.fetchall()
    return {"info":data}

@app.get("/api/v1/teachers")
async def main():
    
    cursor.execute("select * from teachers")
    data=cursor.fetchall()
    
    return {"info":data}



@app.post("/api/v1/add-student", status_code=status.HTTP_201_CREATED)
async def post(name:str,age:int,height:str):
    cursor.execute("insert into students(name,age,height) values(%s,%s,%s)",(name,age,height))
    db.commit()
    return {"name":name,"age":age,"height":height}

@app.options("/api")
async def main():
    return PermissionError
@app.put("/api/v1/students")
async def main():
    return PermissionError

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8000)
