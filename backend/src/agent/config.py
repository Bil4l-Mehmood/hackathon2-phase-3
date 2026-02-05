"""
OpenAI Agent Configuration for Phase III Todo AI Chatbot.
Implements Section 8.5: OpenAI Agent Configuration Prompt

Agent Responsibilities per Section 5:
1. Always infer intent before responding
2. Never manipulate tasks directly; always call MCP tools
3. If required parameters are missing, ask a clarifying question
4. After every tool call, confirm the action in natural language
5. On errors (e.g., task not found), respond politely and suggest next steps

Configuration Requirements (Section 8.5):
- Register all MCP tools
- Enable tool-call logging
- Do not store memory in the agent
"""

import cohere
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize Cohere client
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    # Fallback to OpenAI key if user put cohere key in there by mistake or explicitly ask
    print("Warning: COHERE_API_KEY not found. Please set it in .env")

client = cohere.Client(api_key=api_key)

# Agent system instructions
AGENT_INSTRUCTIONS = """
You are a helpful Todo assistant that manages tasks via natural language.

CRITICAL RULES:
1. Always infer the user's intent before responding
2. NEVER manipulate tasks directly - you MUST use the provided tools for ALL task operations
3. If required parameters are missing, ask a clarifying question
4. After EVERY tool call, confirm the action in natural language
5. On errors (e.g., task not found), respond politely and suggest next steps

AVAILABLE OPERATIONS:
- Create tasks: Use add_task tool (triggers: create/add/remember)
- List tasks: Use list_tasks tool (triggers: list/show/see)
- Complete tasks: Use complete_task tool (triggers: done/complete/finished)
- Delete tasks: Use delete_task tool (triggers: delete/remove/cancel)
- Update tasks: Use update_task tool (triggers: update/change/rename)
"""

# Cohere-formatted tools (List of dicts)
TOOLS = [
    {
        "name": "add_task",
        "description": "Create a new task for the user. Trigger words: create, add, remember.",
        "parameter_definitions": {
            "user_id": {
                "description": "The ID of the user creating the task",
                "type": "str",
                "required": True
            },
            "title": {
                "description": "The title of the task",
                "type": "str",
                "required": True
            },
            "description": {
                "description": "Optional description or details about the task",
                "type": "str",
                "required": False
            }
        }
    },
    {
        "name": "list_tasks",
        "description": "List all tasks for a user. Trigger words: list, show, see.",
        "parameter_definitions": {
            "user_id": {
                "description": "The ID of the user",
                "type": "str",
                "required": True
            },
            "status": {
                "description": "Optional filter: 'completed' for done tasks, 'pending' for active tasks",
                "type": "str",
                "required": False
            }
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a task as completed. Trigger words: done, complete, finished.",
        "parameter_definitions": {
            "user_id": {
                "description": "The ID of the user",
                "type": "str",
                "required": True
            },
            "task_id": {
                "description": "The ID of the task to complete",
                "type": "int",
                "required": True
            }
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task permanently. Trigger words: delete, remove, cancel.",
        "parameter_definitions": {
            "user_id": {
                "description": "The ID of the user",
                "type": "str",
                "required": True
            },
            "task_id": {
                "description": "The ID of the task to delete",
                "type": "int",
                "required": True
            }
        }
    },
    {
        "name": "update_task",
        "description": "Update a task's title or description. Trigger words: update, change, rename.",
        "parameter_definitions": {
            "user_id": {
                "description": "The ID of the user",
                "type": "str",
                "required": True
            },
            "task_id": {
                "description": "The ID of the task to update",
                "type": "int",
                "required": True
            },
            "title": {
                "description": "New title for the task (optional)",
                "type": "str",
                "required": False
            },
            "description": {
                "description": "New description for the task (optional)",
                "type": "str",
                "required": False
            }
        }
    }
]

def get_agent_config() -> dict:
    """
    Get agent configuration for Cohere.
    """
    return {
        "model": "command-r-08-2024",  # Updated from deprecated command-r
        "tools": TOOLS,
    }
