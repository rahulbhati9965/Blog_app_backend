from sqlalchemy.orm import Session
from app.models.blog import Blog


def create_blog(db: Session, title: str, content: str, author_id: int):
    blog = Blog(
        title=title,
        content=content,
        author_id=author_id,
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


def get_all_blogs(db: Session):
    return db.query(Blog).order_by(Blog.created_at.desc()).all()
