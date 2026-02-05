"""
Database session and engine configuration.
Stateless database access following Section 2.2 Statelessness Model.
"""

from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Use "postgresql+psycopg2://" for SQLAlchemy if the string starts with "postgres://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# Neon/Serverless optimization: pool_pre_ping checks connection health before use
engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    pool_pre_ping=True, 
    pool_recycle=300  # Recycle connections every 5 minutes
)


def get_session():
    """
    Get database session for dependency injection.
    Stateless per Section 2.2 - no in-memory session state.
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create all database tables from SQLModel metadata."""
    SQLModel.metadata.create_all(engine)
