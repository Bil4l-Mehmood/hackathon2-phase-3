"""
MCP-style Tool: list_tasks
Implements Section 4: MCP Tool Contract - list_tasks
"""

from pydantic import BaseModel
from sqlmodel import Session, select
from ...db.models import Task
from ...db.session import engine


class ListTasksInput(BaseModel):
    """Input schema for list_tasks tool per Section 4"""
    user_id: str
    status: str | None = None


class TaskItem(BaseModel):
    """Individual task in list output"""
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: str
    updated_at: str


class ListTasksOutput(BaseModel):
    """Output schema for list_tasks tool per Section 4"""
    tasks: list[TaskItem]


async def list_tasks_handler(user_id: str, status: str | None = None) -> ListTasksOutput:
    """
    MCP-style tool handler for listing tasks.
    
    Per Section 4 specification:
    - Trigger: list/show/see
    - Input: user_id, status?
    - Output: array of tasks
    """
    with Session(engine) as session:
        # Build query
        query = select(Task).where(Task.user_id == user_id)
        
        # Apply status filter if provided
        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)
        
        # Execute query
        tasks = session.exec(query).all()
        
        # Transform to output schema
        task_items = [
            TaskItem(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at.isoformat(),
                updated_at=task.updated_at.isoformat()
            )
            for task in tasks
        ]
        
        return ListTasksOutput(tasks=task_items)
