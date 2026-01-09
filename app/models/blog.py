from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Blog(Base):
    __tablename__ = "blogs"

    # 🔑 Primary key
    id: Mapped[int] = mapped_column(primary_key=True)

    # 📝 Blog content
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # 👤 Author relationship
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # 🕒 Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # 🛡️ Admin moderation (soft delete)
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Blog id={self.id} title={self.title!r} author_id={self.author_id}>"
