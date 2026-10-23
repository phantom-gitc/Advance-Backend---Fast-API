from sqlmodel import SQLModel, Session, create_engine
from typing import Generator

DATABASE_URL = "sqlite:///./crud.db"

# connect_args={"check_same_thread": False} is required for SQLite with multi-threaded FastAPI
engine = create_engine(
    DATABASE_URL, 
    echo=False, 
    connect_args={"check_same_thread": False}
)

def create_db_and_tables() -> None:
    """Create all tables in the database."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for providing database sessions to endpoints."""
    with Session(engine) as session:
        yield session
