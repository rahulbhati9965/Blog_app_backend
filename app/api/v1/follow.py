from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.core.dependencies import get_current_user
from app.services.follow_service import follow_user, unfollow_user

router = APIRouter(prefix="/follow", tags=["Follow"])


@router.post("/{user_id}")
def follow(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return follow_user(db, current_user.id, user_id)


@router.delete("/{user_id}")
def unfollow(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return unfollow_user(db, current_user.id, user_id)
