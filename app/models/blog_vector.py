from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT
from app.database.base import Base


class BlogVector(Base):
    __tablename__ = "blog_vectors"

    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"), unique=True)
    vector = Column(ARRAY(FLOAT), nullable=False)
