"""
MCP-style Tool: add_task
Implements Section 4: MCP Tool Contract - add_task

Note: Using direct function implementation instead of MCP SDK decorators
to maintain stateless FastAPI compatibility per Section 2.2.

This follows Section 4 contract exactly:
- Input: user_id, title, description?
- Output: task_id, status=created, title
"""

from pydantic import BaseModel
from sqlmodel import Session
from datetime import datetime
from ...db.models import Task
from ...db.session import engine


class AddTaskInput(BaseModel):
    """Input schema for add_task tool per Section 4"""
    user_id: str
    title: str
    description: str | None = None


class AddTaskOutput(BaseModel):
    """Output schema for add_task tool per Section 4"""
    task_id: int
    status: str = "created"
    title: str


async def add_task_handler(user_id: str, title: str, description: str | None = None) -> AddTaskOutput:
    """
    MCP-style tool handler for adding tasks.
    Stateless function per Section 2.2 - database access only.
    
    Per Section 4 specification:
    - Trigger: create/add/remember
    - Input: user_id, title, description?
    - Output: task_id, status=created, title
    """
    with Session(engine) as session:
        # Create new task
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        session.add(task)
        session.commit()
        session.refresh(task)
        
        # Return structured output per Section 4
        return AddTaskOutput(
            task_id=task.id,
            status="created",
            title=task.title
        )
