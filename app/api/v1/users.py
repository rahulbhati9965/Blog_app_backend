from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.deps import get_db
from app.core.dependencies import get_current_user
from app.models.blog import Blog

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at,
    }


@router.get("/me/blogs")
def my_blogs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return (
        db.query(Blog)
        .filter(Blog.author_id == current_user.id)
        .order_by(Blog.created_at.desc())
        .all()
    )
