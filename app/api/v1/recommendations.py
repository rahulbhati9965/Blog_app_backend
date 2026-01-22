from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.services.recommendation_service import get_recommendations
from app.core.dependencies import get_db, get_current_user
from app.schemas.blog import BlogResponse  # assuming you have a BlogResponse Pydantic schema

router = APIRouter()


@router.get("/recommendations", response_model=List[BlogResponse])
def recommendations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    top_k: int = 10,
):
    """
    Return top-N recommended blogs for the current user
    """
    recommended_blogs = get_recommendations(db=db, current_user=current_user, top_k=top_k)
    return recommended_blogs
