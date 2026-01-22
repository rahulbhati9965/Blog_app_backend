# app/models/blog_keyword.py

from sqlalchemy import Column, Integer, String, ForeignKey, Index
from app.database.base import Base

class BlogKeyword(Base):
    __tablename__ = "blog_keywords"

    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False)
    keyword = Column(String(64), nullable=False)

    __table_args__ = (
        Index("ix_blog_keywords_keyword", "keyword"),
        Index("ix_blog_keywords_blog_id", "blog_id"),
    )
