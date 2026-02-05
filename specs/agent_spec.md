# AI Agent Specification

## Overview
An AI-powered chatbot interface for managing todos through natural language. The agent is stateless and relies on a database for context properly.

## Requirements
- **Framework**: Cohere Agent (Replaced OpenAI Agents SDK due to limits)
- **Model**: `command-r` (Tool-use optimized)
- **Protocol**: MCP-compatible tool calling

## Agent Behavior Rules
1. **Intent Inference**: Always infer the user's intent before responding.
2. **Tool Usage**: NEVER manipulate tasks directly - MUST use provided tools.
3. **Clarification**: If required parameters are missing, ask a clarifying question.
4. **Confirmation**: After EVERY tool call, confirm the action in natural language.
5. **Error Handling**: On errors (e.g., task not found), respond politely and suggest next steps.

## Conversation Flow (Stateless Request Cycle)
1. **Receive Request**: `POST /api/{user_id}/chat`
2. **Fetch History**: Retrieve conversation logs from `conversation` and `message` tables.
3. **Build Context**: Construct prompt with system instructions + history + new message.
4. **Run Agent**: Call LLM with tool definitions.
5. **Tool Execution**: If LLM calls tools, execute them locally and feed results back.
6. **Response**: Generate final natural language response.
7. **Persist**: Save new user message and assistant response to DB.
8. **Return**: Send response to client.

## Natural Language Commands
- **Create**: "Add a task to buy groceries" -> `add_task`
- **List**: "Show me all my tasks" -> `list_tasks`
- **Filter**: "What's pending?" -> `list_tasks(status='pending')`
- **Complete**: "Mark task 3 as complete" -> `complete_task(task_id=3)`
- **Delete**: "Delete the meeting task" -> `delete_task`
- **Update**: "Change task 1 to 'Call mom'" -> `update_task`
