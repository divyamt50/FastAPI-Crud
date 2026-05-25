from typing import Annotated
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi.responses import JSONResponse
from schemas import PostCreate, PostResponse, UserCreate, UserResponse, PostUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from db import Base, engine, get_db

Base.metadata.create_all(bind = engine)

app = FastAPI()


@app.get('/')
def get_message():
    return {"message":"hello"}

@app.get('/api/posts', response_model=list[PostResponse])
def get_posts():
    return posts

@app.get('/api/post/{post_id}', response_model = PostResponse)
def get_one_post(post_id:int):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="post not found"
    )

@app.post('/api/post', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post:PostCreate, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.id == post.user_id)
    )

    user_instance = result.scalars().first()

    if not user_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    new_post = models.Post(
        title = post.title,
        content = post.content,
        user_id = post.user_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/api/posts',response_model=list[PostResponse])
def get_all_posts(db:Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Post)
    )

    return result.scalars().all()

@app.get('/api/post/{id}', response_model=PostResponse)
def get_one_post(post_id:int, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Post).where(models.Post.id == post_id)
    )

    post_instance = result.scalars.first()

    if not post_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Post not found"
        )
    return post_instance

@app.put('/api/post_update/{id}', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def put_post(id:int, post_data:PostCreate,db:Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Post).where(models.Post.id == id)
    )
    post_instance = result.scalars().first()

    if not post_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found"
        )
    
    post_instance.title = post_data.title
    post_instance.content = post_data.content
    db.commit()
    db.refresh(post_instance)
    return post_instance

@app.patch('/api/post_patch/{id}', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def post_path(id:int, post_data:PostUpdate, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Post).where(models.Post.id == id)
    )
    post_instance = result.scalars().first()

    if not post_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found"
        )
    
    updated_data = post_data.model_dump(exclude_unset=True)
    for field, value in updated_data.values():
        setattr(post_instance, field, value)

    db.commit()
    db.refresh(post_instance)
    return post_instance

@app.delete('/api/post_delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Post).where(models.Post.id == id)
    )

    post = result.scalars().first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "post not found"
        )
    
    db.delete(post)
    db.commit()
    return None


@app.post("/api/user", response_model=UserResponse, status = status.HTTP_201_CREATED)
def create_user(user:UserCreate, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.username == user.username)
    )

    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    result = db.execute(
        select(models.User).where(models.User.email == user.email)
    )

    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already exists"
        )
    
    new_user = models.User(
        username = user.username,
        email = user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/api/users/{user_id}', response_model=UserResponse)
def get_user(user_id:int, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.id == user_id)
    )

    user_instance = result.scalars().first()
    
    if user_instance:
        return user_instance
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User ID not found"
    )



@app.exception_handler(RequestValidationError)
def validation_exception_handler(request:Request, exception:RequestValidationError):
    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
        content = {"detail": exception.errors()}
    )