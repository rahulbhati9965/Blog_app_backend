from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Query

from app.database.deps import get_db
from app.schemas.blog import BlogCreate, BlogResponse
from app.services.blog_service import (
    create_blog,
    get_all_blogs,
    update_blog,
    delete_blog,
)
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.post("/", response_model=BlogResponse)
def create(
    data: BlogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_blog(db, data.title, data.content, current_user.id)


@router.get("/", response_model=list[BlogResponse])
def list_all(
    limit: int = Query(10, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return get_all_blogs(db, limit, offset)


@router.put("/{blog_id}", response_model=BlogResponse)
def update(
    blog_id: int,
    data: BlogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_blog(
        db=db,
        blog_id=blog_id,
        title=data.title,
        content=data.content,
        current_user_id=current_user.id,
    )


@router.delete("/{blog_id}")
def delete(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return delete_blog(db, blog_id, current_user.id)
