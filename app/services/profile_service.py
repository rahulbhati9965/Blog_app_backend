from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.follow import Follow
from app.models.blog import Blog


def get_user_profile(
    db: Session,
    profile_user_id: int,
    current_user_id: int,
):
    user = db.get(User, profile_user_id)
    if not user:
        return None

    followers_count = (
        db.query(func.count(Follow.id))
        .filter(Follow.following_id == profile_user_id)
        .scalar()
    )

    following_count = (
        db.query(func.count(Follow.id))
        .filter(Follow.follower_id == profile_user_id)
        .scalar()
    )

    is_following = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user_id,
            Follow.following_id == profile_user_id,
        )
        .first()
        is not None
    )

    blogs = (
        db.query(Blog)
        .filter(Blog.author_id == profile_user_id)
        .order_by(Blog.created_at.desc())
        .all()
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
        "blogs": blogs,
    }
