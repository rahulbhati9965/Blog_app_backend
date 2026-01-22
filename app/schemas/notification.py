from pydantic import BaseModel
from datetime import datetime


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    actor_id: int
    type: str
    entity_id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
