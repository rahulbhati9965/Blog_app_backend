from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import func
from app.services.notification_service import create_notification
from app.models.like import Like
from app.models.blog import Blog


def like_blog(db: Session, user_id: int, blog_id: int):
    blog = db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found",
        )

    existing = (
        db.query(Like)
        .filter(
            Like.user_id == user_id,
            Like.blog_id == blog_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already liked",
        )

    like = Like(user_id=user_id, blog_id=blog_id)
    db.add(like)
    db.commit()
    create_notification(
    db=db,
    user_id=blog.author_id,
    actor_id=user_id,
    type_="like",
    entity_id=blog_id,
)

    return {"message": "Blog liked"}


def unlike_blog(db: Session, user_id: int, blog_id: int):
    like = (
        db.query(Like)
        .filter(
            Like.user_id == user_id,
            Like.blog_id == blog_id,
        )
        .first()
    )

    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Like not found",
        )

    db.delete(like)
    db.commit()
    return {"message": "Like removed"}


def get_like_count(db: Session, blog_id: int):
    return (
        db.query(func.count(Like.id))
        .filter(Like.blog_id == blog_id)
        .scalar()
    )


