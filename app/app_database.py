import os
from collections.abc import Generator

from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

# Uses the environment variable from docker-compose.yml
# Fallback for local testing if running outside docker
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/albumbot"
)

engine = create_engine(DATABASE_URL)

def init_db() -> None:
    # Execute raw SQL to create the pgvector extension if it doesn't exist
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    # Create all SQLModel tables (Album, VectorStore, etc) defined in models.py
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
