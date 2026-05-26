from __future__ import annotations



from pydantic import ConfigDict, BaseModel, Field, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title:str= Field(min_length=2, max_length=20)
    content:str = Field(min_length=10, max_length=1000)

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id:int
    date_posted:str
    user_id:int
    author: UserResponse

class PostUpdate(PostBase):
    title:str|None = Field(default = None, min_length=1, max_length=100)
    content:str|None = Field(default= None, min_length=1)


class UserBase(BaseModel):
    username:str = Field(min_length=2, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password:str = Field(min_length=5)

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id:int

class Token(BaseModel):
    access_token: str
    token_type: str