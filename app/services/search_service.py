from sqlalchemy.orm import Session
from app.models.blog import Blog
from app.models.user import User


def search_blogs(
    db: Session,
    query: str,
    limit: int = 10,
    offset: int = 0,
):
    return (
        db.query(Blog)
        .filter(
            Blog.title.ilike(f"%{query}%")
            | Blog.content.ilike(f"%{query}%")
        )
        .order_by(Blog.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

def search_users(
    db: Session,
    query: str,
    limit: int = 10,
    offset: int = 0,
):
    return (
        db.query(User)
        .filter(
            User.username.ilike(f"%{query}%")
            | User.email.ilike(f"%{query}%")
        )
        .limit(limit)
        .offset(offset)
        .all()
    )
