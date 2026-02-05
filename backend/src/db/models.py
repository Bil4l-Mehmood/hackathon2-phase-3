"""
Database models for Phase III Todo AI Chatbot.
Implements Section 3: Data Model Specification from SPECIFICATION.md

Following Section 8.2 Database Models & Migration Prompt:
- Use SQLModel and PostgreSQL-compatible types
- Include timestamps and indexes as specified
- Enforce foreign key relationships
- No business logic or API endpoints
"""

from datetime import datetime
from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship


class MessageRole(str, Enum):
    """Message role enum as specified in Section 3"""
    USER = "user"
    ASSISTANT = "assistant"


class Task(SQLModel, table=True):
    """
    Task model per Section 3 specification.
    
    Fields:
    - id (int, PK)
    - user_id (string, indexed)
    - title (string)
    - description (string, nullable)
    - completed (bool, default false)
    - created_at (datetime)
    - updated_at (datetime)
    """
    __tablename__ = "task"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Conversation(SQLModel, table=True):
    """
    Conversation model per Section 3 specification.
    
    Fields:
    - id (int, PK)
    - user_id (string, indexed)
    - created_at (datetime)
    - updated_at (datetime)
    """
    __tablename__ = "conversation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to messages
    messages: list["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """
    Message model per Section 3 specification.
    
    Fields:
    - id (int, PK)
    - conversation_id (FK)
    - user_id (string)
    - role (enum: user | assistant)
    - content (text)
    - created_at (datetime)
    """
    __tablename__ = "message"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    user_id: str
    role: MessageRole
    content: str  # TEXT type in PostgreSQL
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
