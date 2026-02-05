"""
MCP-style Tool: delete_task
Implements Section 4: MCP Tool Contract - delete_task
"""

from pydantic import BaseModel
from sqlmodel import Session
from ...db.models import Task
from ...db.session import engine


class DeleteTaskInput(BaseModel):
    """Input schema for delete_task tool per Section 4"""
    user_id: str
    task_id: int


class DeleteTaskOutput(BaseModel):
    """Output schema for delete_task tool per Section 4"""
    task_id: int
    status: str = "deleted"
    title: str


async def delete_task_handler(user_id: str, task_id: int) -> DeleteTaskOutput:
    """
    MCP-style tool handler for deleting tasks.
    
    Per Section 4 specification:
    - Trigger: delete/remove/cancel
    - Input: user_id, task_id
    - Output: task_id, status=deleted, title
    """
    with Session(engine) as session:
        # Fetch task
        task = session.get(Task, task_id)
        
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Validate ownership
        if task.user_id != user_id:
            raise ValueError(f"Task {task_id} does not belong to user {user_id}")
        
        # Save title before deletion
        task_title = task.title
        task_id_value = task.id
        
        # Delete task
        session.delete(task)
        session.commit()
        
        # Return structured output per Section 4
        return DeleteTaskOutput(
            task_id=task_id_value,
            status="deleted",
            title=task_title
        )
