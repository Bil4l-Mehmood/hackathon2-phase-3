"""
MCP-style Tool: complete_task
Implements Section 4: MCP Tool Contract - complete_task
"""

from pydantic import BaseModel
from sqlmodel import Session
from datetime import datetime
from ...db.models import Task
from ...db.session import engine


class CompleteTaskInput(BaseModel):
    """Input schema for complete_task tool per Section 4"""
    user_id: str
    task_id: int


class CompleteTaskOutput(BaseModel):
    """Output schema for complete_task tool per Section 4"""
    task_id: int
    status: str = "completed"
    title: str


async def complete_task_handler(user_id: str, task_id: int) -> CompleteTaskOutput:
    """
    MCP-style tool handler for completing tasks.
    
    Per Section 4 specification:
    - Trigger: done/complete/finished
    - Input: user_id, task_id
    - Output: task_id, status=completed, title
    """
    with Session(engine) as session:
        # Fetch task
        task = session.get(Task, task_id)
        
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Validate ownership
        if task.user_id != user_id:
            raise ValueError(f"Task {task_id} does not belong to user {user_id}")
        
        # Mark as completed
        task.completed = True
        task.updated_at = datetime.utcnow()
        
        session.add(task)
        session.commit()
        session.refresh(task)
        
        # Return structured output per Section 4
        return CompleteTaskOutput(
            task_id=task.id,
            status="completed",
            title=task.title
        )
