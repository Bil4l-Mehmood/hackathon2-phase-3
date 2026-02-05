# MCP Tools Specification

The MCP server exposes the following tools for the AI agent to manage tasks.

## 1. add_task
- **Purpose**: Create a new task
- **Parameters**: 
  - `user_id` (string, required)
  - `title` (string, required)
  - `description` (string, optional)
- **Returns**: `task_id`, `status`, `title`

## 2. list_tasks
- **Purpose**: Retrieve tasks from the list
- **Parameters**: 
  - `user_id` (string, required)
  - `status` (string, optional: "all", "pending", "completed")
- **Returns**: Array of task objects `[{"id": 1, ...}]`

## 3. complete_task
- **Purpose**: Mark a task as complete
- **Parameters**: 
  - `user_id` (string, required)
  - `task_id` (integer, required)
- **Returns**: `task_id`, `status`, `title`

## 4. delete_task
- **Purpose**: Remove a task from the list
- **Parameters**: 
  - `user_id` (string, required)
  - `task_id` (integer, required)
- **Returns**: `task_id`, `status`, `title`

## 5. update_task
- **Purpose**: Modify task title or description
- **Parameters**: 
  - `user_id` (string, required)
  - `task_id` (integer, required)
  - `title` (string, optional)
  - `description` (string, optional)
- **Returns**: `task_id`, `status`, `title`

## Architecture
Tools are implemented as Python functions in `src/mcp/tools/` and exposed directly to the Agent runner. State is persisted in the PostgreSQL database via SQLModel.
