from sqlalchemy.orm import Session
from app.models.notification import Notification


def create_notification(
    db: Session,
    user_id: int,
    actor_id: int,
    type_: str,
    entity_id: int,
):
    if user_id == actor_id:
        return  # no self-notifications

    notification = Notification(
        user_id=user_id,
        actor_id=actor_id,
        type=type_,
        entity_id=entity_id,
    )
    db.add(notification)
    db.commit()


def get_notifications(db: Session, user_id: int):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def mark_as_read(db: Session, notification_id: int, user_id: int):
    notification = db.get(Notification, notification_id)

    if not notification or notification.user_id != user_id:
        return None

    notification.is_read = True
    db.commit()
    return notification
