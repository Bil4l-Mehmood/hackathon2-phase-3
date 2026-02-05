"""
Cohere Agent Runner - handles tool invocation and response generation.
Stateless per Section 2.2 - no memory stored in agent.
"""

import logging
import json
import cohere
from .config import client, AGENT_INSTRUCTIONS, get_agent_config
from ..mcp.tools import (
    add_task_handler,
    list_tasks_handler,
    complete_task_handler,
    delete_task_handler,
    update_task_handler
)

logger = logging.getLogger(__name__)


async def execute_tool_call(tool_name: str, arguments: dict) -> list[dict]:
    """
    Execute MCP tool based on function call from agent.
    Returns the result formatted for Cohere tool outputs.
    """
    try:
        logger.info(f"Executing tool: {tool_name} with args: {arguments}")
        
        result_data = {}
        if tool_name == "add_task":
            result = await add_task_handler(**arguments)
            result_data = result.model_dump()
        
        elif tool_name == "list_tasks":
            result = await list_tasks_handler(**arguments)
            result_data = result.model_dump()
        
        elif tool_name == "complete_task":
            result = await complete_task_handler(**arguments)
            result_data = result.model_dump()
        
        elif tool_name == "delete_task":
            result = await delete_task_handler(**arguments)
            result_data = result.model_dump()
        
        elif tool_name == "update_task":
            result = await update_task_handler(**arguments)
            result_data = result.model_dump()
        else:
            result_data = {"error": f"Unknown tool: {tool_name}"}
            
        return [result_data]
            
    except Exception as e:
        logger.error(f"Tool execution error: {str(e)}")
        return [{"error": str(e)}]


async def run_agent(messages: list[dict]) -> tuple[str, list[dict]]:
    """
    Run Cohere Agent with conversation history.
    """
    agent_config = get_agent_config()
    
    # Convert OpenAI-style messages to Cohere chat_history
    chat_history = []
    message_input = ""
    
    # The last message is the current user input
    if messages and messages[-1]['role'] == 'user':
        message_input = messages[-1]['content']
        history_messages = messages[:-1]
    else:
        # Should not happen ideally, but handle gracefully
        history_messages = messages
        
    for msg in history_messages:
        role = msg['role']
        content = msg['content']
        
        if role == 'user':
            chat_history.append({"role": "USER", "message": content})
        elif role == 'assistant':
            chat_history.append({"role": "CHATBOT", "message": content})
        # System messages are passed in preamble, not history
            
    try:
        # Initial prediction
        response = client.chat(
            message=message_input,
            chat_history=chat_history,
            preamble=AGENT_INSTRUCTIONS,
            **agent_config
        )
        
        tool_calls_made = []
        
        # Handle tool calls loop (multi-step capability)
        while response.tool_calls:
            tool_results = []
            
            for tool_call in response.tool_calls:
                header = f"Tool Call: {tool_call.name}"
                logger.info(header)
                
                # Execute tool
                outputs = await execute_tool_call(tool_call.name, tool_call.parameters)
                
                # Add to results for Cohere
                tool_results.append({
                    "call": tool_call,
                    "outputs": outputs
                })
                
                # Track for frontend transparency
                tool_calls_made.append({
                    "tool": tool_call.name,
                    "arguments": tool_call.parameters,
                    "result": outputs[0]
                })

            # Send tool results back to Cohere to generate final response
            response = client.chat(
                message="", # Continuation
                chat_history=chat_history, # Logic handled by client state usually, but for stateless we might need to rely on the response object method if using SDK stateful client, OR provide tool_results.
                # Cohere Python SDK 'chat' is stateless if no conversation_id is passed, but we need to pass back tool results.
                # The recommendation is to use the `tool_results` parameter in the next call.
                tool_results=tool_results,
                preamble=AGENT_INSTRUCTIONS,
                model=agent_config["model"],
                tools=agent_config["tools"]
            )
            
        return response.text, tool_calls_made

    except Exception as e:
        logger.error(f"Cohere API Error: {str(e)}")
        return f"I encountered an error with the AI service: {str(e)}", []
