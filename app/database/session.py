import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Render + production standard
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(
    DATABASE_URL,
    echo=False,   # IMPORTANT: keep False in production
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
