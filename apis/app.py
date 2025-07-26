#! /usr/bin/python3
from fastapi import FastAPI

app = FastAPI()


@app.get("/")

def home_page():
    return {"message":"api working"}