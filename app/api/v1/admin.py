from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.core.admin_dependency import get_admin_user
from app.services.admin_service import (
    ban_user,
    unban_user,
    soft_delete_blog,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/ban-user/{user_id}")
def ban(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return ban_user(db, user_id)


@router.post("/unban-user/{user_id}")
def unban(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return unban_user(db, user_id)


@router.delete("/blog/{blog_id}")
def remove_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return soft_delete_blog(db, blog_id)
