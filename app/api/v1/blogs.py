from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.blog import BlogCreate, BlogResponse
from app.services.blog_service import create_blog, get_all_blogs
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
def list_all(db: Session = Depends(get_db)):
    return get_all_blogs(db)
