from sqlalchemy.orm import Session
from app.models.blog import Blog
from fastapi import HTTPException, status
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

def get_all_blogs(
    db: Session,
    limit: int = 10,
    offset: int = 0,
):
    return (
        db.query(Blog)
        .order_by(Blog.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )




def get_blog_by_id(db, blog_id: int):
    return db.get(Blog, blog_id)


def update_blog(
    db,
    blog_id: int,
    title: str,
    content: str,
    current_user_id: int,
):
    blog = get_blog_by_id(db, blog_id)

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found",
        )

    if blog.author_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this blog",
        )

    blog.title = title
    blog.content = content

    db.commit()
    db.refresh(blog)
    return blog


def delete_blog(db, blog_id: int, current_user_id: int):
    blog = get_blog_by_id(db, blog_id)

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found",
        )

    if blog.author_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this blog",
        )

    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}


def get_blog_by_id(db: Session, blog_id: int) -> Blog:
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found",
        )

    return blog