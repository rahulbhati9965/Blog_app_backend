from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.follow import Follow
from app.services.notification_service import create_notification


def follow_user(
    db: Session,
    follower_id: int,
    following_id: int,
):
    if follower_id == following_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow yourself",
        )

    existing = (
        db.query(Follow)
        .filter(
            Follow.follower_id == follower_id,
            Follow.following_id == following_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already following this user",
        )

    follow = Follow(
        follower_id=follower_id,
        following_id=following_id,
    )
    db.add(follow)
    db.commit()

    # 🔔 NOTIFICATION (✅ correct place)
    create_notification(
        db=db,
        user_id=following_id,
        actor_id=follower_id,
        type_="follow",
        entity_id=follower_id,
    )

    return {"message": "User followed successfully"}


def unfollow_user(
    db: Session,
    follower_id: int,
    following_id: int,
):
    follow = (
        db.query(Follow)
        .filter(
            Follow.follower_id == follower_id,
            Follow.following_id == following_id,
        )
        .first()
    )

    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not following this user",
        )

    db.delete(follow)
    db.commit()
    return {"message": "User unfollowed successfully"}
