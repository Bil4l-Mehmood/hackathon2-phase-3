"""
Database dependency injection for MCP tools.
Provides stateless database access per Section 2.2.
"""

from sqlmodel import Session
from ..db.session import engine


def get_db_session() -> Session:
    """
    Dependency injection for database session in MCP tools.
    Stateless: each tool invocation gets a fresh session.
    """
    with Session(engine) as session:
        yield session
