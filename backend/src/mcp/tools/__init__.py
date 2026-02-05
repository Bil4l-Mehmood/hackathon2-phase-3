"""MCP-style Tools package initialization - all 5 task operation tools"""

from .add_task import add_task_handler, AddTaskInput, AddTaskOutput
from .list_tasks import list_tasks_handler, ListTasksInput, ListTasksOutput
from .complete_task import complete_task_handler, CompleteTaskInput, CompleteTaskOutput
from .delete_task import delete_task_handler, DeleteTaskInput, DeleteTaskOutput
from .update_task import update_task_handler, UpdateTaskInput, UpdateTaskOutput

# Export all handlers per Section 4 contract
__all__ = [
    # add_task
    "add_task_handler",
    "AddTaskInput",
    "AddTaskOutput",
    # list_tasks
    "list_tasks_handler",
    "ListTasksInput",
    "ListTasksOutput",
    # complete_task
    "complete_task_handler",
    "CompleteTaskInput",
    "CompleteTaskOutput",
    # delete_task
    "delete_task_handler",
    "DeleteTaskInput",
    "DeleteTaskOutput",
    # update_task
    "update_task_handler",
    "UpdateTaskInput",
    "UpdateTaskOutput",
]
