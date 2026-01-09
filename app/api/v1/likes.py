from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.core.dependencies import get_current_user
from app.services.like_service import (
    like_blog,
    unlike_blog,
    get_like_count,
)

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/blog/{blog_id}")
def like(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return like_blog(db, current_user.id, blog_id)


@router.delete("/blog/{blog_id}")
def unlike(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return unlike_blog(db, current_user.id, blog_id)


@router.get("/blog/{blog_id}/count")
def count(blog_id: int, db: Session = Depends(get_db)):
    return {"likes": get_like_count(db, blog_id)}
