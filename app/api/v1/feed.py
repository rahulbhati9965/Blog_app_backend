from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.core.dependencies import get_current_user
from app.schemas.blog import BlogResponse
from app.services.feed_service import get_feed

router = APIRouter(prefix="/feed", tags=["Feed"])


@router.get("/", response_model=list[BlogResponse])
def feed(
    limit: int = Query(10, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_feed(db, current_user.id, limit, offset)
