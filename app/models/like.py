from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database.base import Base


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    blog_id: Mapped[int] = mapped_column(
        ForeignKey("blogs.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "blog_id",
            name="unique_blog_like",
        ),
    )
