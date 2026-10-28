"""Database — SQLAlchemy. SQLite by default, PostgreSQL + pgvector via DATABASE_URL."""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def is_postgres() -> bool:
    """True when the app is running against PostgreSQL (pgvector mode)."""
    return settings.database_url.startswith(("postgres://", "postgresql://"))


def get_db():
    """FastAPI dependency: one DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables (no migrations needed for this project size).

    On PostgreSQL this also enables the pgvector extension first, so the
    Chunk.embedding Vector(384) column and its HNSW index can be created.
    """
    from . import models  # noqa: F401  (import registers the models)

    if is_postgres():
        with engine.begin() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(bind=engine)
