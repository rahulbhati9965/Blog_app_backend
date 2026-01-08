from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repo import get_user_by_email, create_user
from app.core.security import hash_password, verify_password, create_access_token


def register_user(db: Session, username: str, email: str, password: str):
    existing = get_user_by_email(db, email)
    if existing:
        raise ValueError("Email already registered")

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )
    return create_user(db, user)


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return token
