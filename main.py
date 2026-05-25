from typing import Annotated
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi.responses import JSONResponse
from schemas import PostCreate, PostResponse, UserCreate, UserResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from db import Base, engine, get_db

Base.metadata.create_all(bind = engine)

app = FastAPI()

posts:list[dict] = [
    {
        "id":1,
        "title":"First blog",
        "description":"this is my first blog",
        "author":"Divyam",
        "date_posted":"27 March 2027"
    },
    {
        "id":2,
        "title":"Second blog",
        "description":"this is my second blog",
        "author":"Divyam",
        "date_posted":"27 March 2027"
    },
    {
        "id":3,
        "title":"Third blog",
        "description":"this is my third blog",
        "author":"Divyam",
        "date_posted":"27 March 2027"
    },
    {
        "id":4,
        "title":"Fourth blog",
        "description":"this is my fourth blog",
        "author":"Divyam",
        "date_posted":"27 March 2027"
    },
    {
        "id":5,
        "title":"Fifth blog",
        "description":"this is my fifth blog",
        "author":"Divyam",
        "date_posted":"27 March 2027"
    }
]

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

@app.post('/api/post', response_model=PostResponse)
def add_post(post:PostCreate):
    new_post = {
            "id":len(posts) + 1,
            "title":post.title,
            "description":post.description,
            "author":post.author,
            "date_posted":"27 March 2027"
        }
    posts.append(new_post)
    return new_post

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
        content = {"detail":exception.errors()}
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request:Request, exception:RequestValidationError):
    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
        content = {"detail": exception.errors()}
    )