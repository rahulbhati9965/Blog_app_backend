from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.services.notification_service import create_notification
from app.models.comment import Comment
from app.models.blog import Blog

def add_comment(
    db: Session,
    content: str,
    user_id: int,
    blog_id: int,
):
    blog = db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found",
        )

    comment = Comment(
        content=content,
        user_id=user_id,
        blog_id=blog_id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    # 🔔 NOTIFICATION (✅ correct place)
    create_notification(
        db=db,
        user_id=blog.author_id,
        actor_id=user_id,
        type_="comment",
        entity_id=blog_id,
    )

    return comment


def get_comments_for_blog(
    db: Session,
    blog_id: int,
    limit: int = 10,
    offset: int = 0,
):
    return (
        db.query(Comment)
        .filter(Comment.blog_id == blog_id)
        .order_by(Comment.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )



def delete_comment(
    db: Session,
    comment_id: int,
    current_user_id: int,
):
    comment = db.get(Comment, comment_id)

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    if comment.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this comment",
        )

    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}


def get_commented_blogs_by_user(db: Session, user_id: int):
    return (
        db.query(Blog)
        .join(Comment, Blog.id == Comment.blog_id)
        .filter(Comment.user_id == user_id, Blog.is_deleted == False)
        .all()
    )


