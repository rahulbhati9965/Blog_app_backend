from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.user import UserSearchResponse
from app.services.search_service import search_users
from app.database.deps import get_db
from app.schemas.blog import BlogResponse
from app.services.search_service import search_blogs

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/blogs", response_model=list[BlogResponse])
def search_blog_endpoint(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return search_blogs(db, q, limit, offset)



@router.get("/users", response_model=list[UserSearchResponse])
def search_user_endpoint(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return search_users(db, q, limit, offset)
