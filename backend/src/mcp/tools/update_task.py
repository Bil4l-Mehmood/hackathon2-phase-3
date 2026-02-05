"""
MCP-style Tool: update_task
Implements Section 4: MCP Tool Contract - update_task
"""

from pydantic import BaseModel
from sqlmodel import Session
from datetime import datetime
from ...db.models import Task
from ...db.session import engine


class UpdateTaskInput(BaseModel):
    """Input schema for update_task tool per Section 4"""
    user_id: str
    task_id: int
    title: str | None = None
    description: str | None = None


class UpdateTaskOutput(BaseModel):
    """Output schema for update_task tool per Section 4"""
    task_id: int
    status: str = "updated"
    title: str


async def update_task_handler(
    user_id: str, 
    task_id: int, 
    title: str | None = None, 
    description: str | None = None
) -> UpdateTaskOutput:
    """
    MCP-style tool handler for updating tasks.
    
    Per Section 4 specification:
    - Trigger: update/change/rename
    - Input: user_id, task_id, title?, description?
    - Output: task_id, status=updated, title
    """
    with Session(engine) as session:
        # Fetch task
        task = session.get(Task, task_id)
        
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Validate ownership
        if task.user_id != user_id:
            raise ValueError(f"Task {task_id} does not belong to user {user_id}")
        
        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        
        task.updated_at = datetime.utcnow()
        
        session.add(task)
        session.commit()
        session.refresh(task)
        
        # Return structured output per Section 4
        return UpdateTaskOutput(
            task_id=task.id,
            status="updated",
            title=task.title
        )
