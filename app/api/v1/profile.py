from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.core.dependencies import get_current_user
from app.schemas.profile import UserProfileResponse
from app.services.profile_service import get_user_profile

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/{user_id}", response_model=UserProfileResponse)
def profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    profile = get_user_profile(db, user_id, current_user.id)

    if not profile:
        raise HTTPException(status_code=404, detail="User not found")

    return profile
