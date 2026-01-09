from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Query
from app.database.deps import get_db
from app.core.dependencies import get_current_user
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment_service import (
    add_comment,
    get_comments_for_blog,
    delete_comment,
)

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/blog/{blog_id}", response_model=CommentResponse)
def create_comment(
    blog_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return add_comment(db, data.content, current_user.id, blog_id)




@router.get("/blog/{blog_id}", response_model=list[CommentResponse])
def list_comments(
    blog_id: int,
    limit: int = Query(10, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return get_comments_for_blog(db, blog_id, limit, offset)



@router.delete("/{comment_id}")
def delete(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return delete_comment(db, comment_id, current_user.id)
