#! /usr/bin/python3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL='mysql+pymysql://root:king@localhost/jayleens'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
Base=declarative_base()

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    try:
        db=SessionLocal()
        yield db
        
    finally:
        db.close()
