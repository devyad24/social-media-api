from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

##pydantic model defining the shape of the request, it basically validates the request

##request schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True  ##read data even if its not a dict

##response schemas
class Post(PostBase):
    id: int
    created_at: datetime 
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

##user schemas

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None 

#vote schemas

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0,le=1) #specifying like/unlike system i.e if 0 then not liked and vice-versa