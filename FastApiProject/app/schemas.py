from datetime import datetime
from typing import List, Optional

from fastapi_pagination import Page
from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict, EmailStr


class UserRead(schemas.BaseUser[int]):
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr


class UserShort(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class GroupRead(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    model_config = ConfigDict(from_attributes=True)


class PostCreate(BaseModel):
    text: str
    group_id: Optional[int] = None
    image: Optional[str] = None


class CommentCreate(BaseModel):
    text: str


class CommentRead(CommentCreate):
    id: int
    pub_date: datetime
    author: Optional[UserRead] = None
    model_config = ConfigDict(from_attributes=True)


class PostList(BaseModel):
    id: int
    text: str
    pub_date: datetime
    image: Optional[str] = None
    author: UserRead
    author_id: int
    group_id: Optional[int] = None
    group: Optional[GroupRead] = None
    model_config = ConfigDict(from_attributes=True)


class PostDetail(BaseModel):
    id: int
    text: str
    pub_date: datetime
    image: Optional[str] = None
    author: UserRead
    group: Optional[GroupRead] = None
    comments: List[CommentRead] = []
    model_config = ConfigDict(from_attributes=True)


class PostDetailResponse(BaseModel):
    post: PostDetail
    author_post_count: int


class ProfileResponse(BaseModel):
    author: UserRead
    posts: Page[PostList]
    is_following: bool
    total_posts: int
    model_config = ConfigDict(from_attributes=True)


class GroupCreate(BaseModel):
    title: str
    slug: str
    description: str = ""


class GroupPostsResponse(BaseModel):
    group: GroupRead
    posts: Page[PostList]
