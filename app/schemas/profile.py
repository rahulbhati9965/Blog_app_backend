from pydantic import BaseModel
from typing import List
from app.schemas.blog import BlogResponse


class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    followers_count: int
    following_count: int
    is_following: bool
    blogs: List[BlogResponse]

    class Config:
        from_attributes = True

