from pydantic import ConfigDict, BaseModel, Field


class PostBase(BaseModel):
    title:str= Field(min_length=2, max_length=20)
    content:str = Field(min_length=10, max_length=1000)
    author:str=Field(min_length = 2, max_length=40)

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id:int
    date_posted:str