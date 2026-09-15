from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=10)


class PostUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=10)


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    image: str | None = None
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PaginatedPostResponse(BaseModel):
    posts: list[PostResponse]
    total: int
    page: int
    limit: int
    total_pages: int

class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=1000)

class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True

class LikeResponse(BaseModel):
    id: int
    post_id: int
    user_id: int

    class Config:
        from_attributes = True