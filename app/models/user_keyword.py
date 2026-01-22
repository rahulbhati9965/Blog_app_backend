from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

class UserKeyword(Base):
    __tablename__ = "user_keywords"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    keyword: Mapped[str] = mapped_column(String(100), nullable=False)
    weight: Mapped[float] = mapped_column(default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
