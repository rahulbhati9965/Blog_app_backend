from pydantic import BaseModel
from app.services.blog_service import (
    create_blog,
    get_all_blogs,
    update_blog,
    delete_blog,
)



class BlogCreate(BaseModel):
    title: str
    content: str


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int

    class Config:
        from_attributes = True
