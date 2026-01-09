from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.models.blog import Blog


def ban_user(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.is_banned = True
    db.commit()
    return {"message": "User banned successfully"}


def unban_user(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.is_banned = False
    db.commit()
    return {"message": "User unbanned successfully"}


def soft_delete_blog(db: Session, blog_id: int):
    blog = db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(404, "Blog not found")

    blog.is_deleted = True
    db.commit()
    return {"message": "Blog removed by admin"}
