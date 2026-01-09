from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.core.dependencies import get_current_user
from app.schemas.notification import NotificationResponse
from app.services.notification_service import (
    get_notifications,
    mark_as_read,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=list[NotificationResponse])
def list_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_notifications(db, current_user.id)


@router.post("/{notification_id}/read")
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return mark_as_read(db, notification_id, current_user.id)
