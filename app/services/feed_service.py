from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.blog import Blog
from app.models.follow import Follow


def get_feed(
    db: Session,
    user_id: int,
    limit: int = 10,
    offset: int = 0,
):
    followed_subquery = (
        select(Follow.following_id)
        .where(Follow.follower_id == user_id)
    )

    stmt = (
        select(Blog)
        .where(
            (Blog.author_id == user_id)
            | (Blog.author_id.in_(followed_subquery))
        )
        .order_by(Blog.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    return db.execute(stmt).scalars().all()
