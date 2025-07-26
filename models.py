#! /usr/bin/python3
import sqlalchemy.orm
from database import Base
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
import sqlalchemy
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__='users'
    id=sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,index=True)
    username=sqlalchemy.Column(sqlalchemy.String(length=255),unique=True,index=True,)
    email=sqlalchemy.Column(sqlalchemy.String(length=255),unique=True,index=True)
    password=sqlalchemy.Column(sqlalchemy.String(length=255))
    isAdmin=sqlalchemy.Column(sqlalchemy.Boolean,default=False)
    joined=sqlalchemy.Column(sqlalchemy.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password
        self.joined=sqlalchemy.func.now()
    
    def __repr__(self):
        return self.username


class Post(Base):
    __tablename__='posts'
    id=sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,index=True)
    title=sqlalchemy.Column(sqlalchemy.String(length=255),unique=True,index=True)
    body=sqlalchemy.Column(sqlalchemy.String(length=255))
    created_at=sqlalchemy.Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    published=sqlalchemy.Column(sqlalchemy.Boolean,default=True)
    owner_id=sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("User")
    def __init__(self,title,body,created_at=sqlalchemy.func.now()):
        self.title=title
        self.body=body
        self.created_at=sqlalchemy.func.now()
        self.published=True

    def __repr__(self):
        return self.title


class Vote(Base):
    __tablename__="votes"
    post_id=sqlalchemy.Column(sqlalchemy.ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    user_id=sqlalchemy.Column(sqlalchemy.ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)