#! usr/bin/python3
from fastapi import FastAPI,Depends,status,APIRouter,HTTPException
from middleware import schemas
from models.database import get_db
from models import models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from middleware.tokens import create_access_token,verify_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(
   
)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

@router.post("/api/v1/oauth2/login")
async def user_login(user:schemas.Login,db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == user.email).first()


    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with such credentials not found")
    
    if not pwd_context.verify(user.password,user_query.password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f'Invalid credentials')

    access_token = create_access_token(data={"id":str(user_query._id)})

    return {"access_token":access_token,"token_type":"Bearer"}
