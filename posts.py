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
    prefix="/api/v1/posts",
    tags=['Posts']
)


@router.get("/",response_model=List[schemas.PostOut],status_code=status.HTTP_200_OK)
async def get_post(db: Session=Depends(get_db),logged_user: int =Depends(tokens.get_current_user)):
    posts=db.query(models.Post).filter(models.Post.owner_id==logged_user.id).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No post retrieved")
    return posts

@router.post("/",response_model=schemas.PostOut)
def main(post: schemas.Post,current_user: int =Depends(tokens.get_current_user), db: Session=Depends(get_db)):
    post=models.Post(title=post.title,body=post.body,owner_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" 404 NOT FOUND")
    return post
@router.put("/{id}")
def main(id:int,post: schemas.Post,db: Session=Depends(get_db),current_user: int =Depends(tokens.get_current_user) ):
    post_query=db.query(models.Post).filter(models.Post.id== id)
    new_post=post_query.first()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" 404 NOT FOUND")
    if new_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You can only update your own posts")
    post_query.update({models.Post.title:post.title,models.Post.body:post.body})
    db.commit()
    return post_query.first()


@router.delete("/{id}")
def main(id:int,db: Session=Depends(get_db), current_user : int = Depends(tokens.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id== id)
    new_post=post_query.first()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" 404 NOT FOUND")
    if new_post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You can only delete your own posts")
    post_query.delete(synchronize_session=False)
    db.commit()
    return post_query.first()