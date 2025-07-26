#! /usr/bin/python3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL=f'mysql+pymysql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}/{settings.DATABASE_NAME}'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
Base=declarative_base()

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()



