import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./sql_app.db"

if os.environ.get("TESTING"):
    engine = create_engine("sqlite:///:memory:")
else:
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_tables():
    """Initializes the database schema (only for local development/SQLite)."""
    Base.metadata.create_all(bind=engine)