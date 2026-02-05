"""
Stateless Chat Endpoint for Phase III Todo AI Chatbot.
Implements Section 8.6: Stateless Chat Endpoint Prompt

Execution Contract per Section 8.6:
1. Accept message and optional conversation_id
2. Fetch conversation history from the database
3. Build agent message array (history + new message)
4. Persist the user message before agent execution
5. Run the OpenAI Agent with MCP tools
6. Persist assistant response and tool call metadata
7. Return conversation_id, response text, and tool_calls
8. Discard all in-memory state after response

Constraints:
- Stateless per request
- No global variables
- No cached sessions
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
import json

from ..db import get_session, Conversation, Message, MessageRole
from ..agent import run_agent

router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request schema per Section 8.6"""
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    """Chat response schema per Section 1.3 and 8.6"""
    conversation_id: int
    response: str
    tool_calls: list[dict]  # Tool calls for transparency per Section 1.3


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_session)
) -> ChatResponse:
    """
    POST /api/{user_id}/chat
    
    Stateless chat endpoint per Section 2.1 and 8.6.
    All state persisted to database, no in-memory session.
    """
    
    # Step 1 & 2: Get or create conversation, load history
    if request.conversation_id:
        # Load existing conversation
        conversation = db.get(Conversation, request.conversation_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        if conversation.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Load message history (Section 2.2: conversation continuity from DB)
        messages_query = select(Message).where(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at)
        history = db.exec(messages_query).all()
        
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        history = []
    
    # Step 3 & 4: Build agent message array and persist user message
    user_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role=MessageRole.USER,
        content=request.message,
        created_at=datetime.utcnow()
    )
    db.add(user_message)
    db.commit()
    
    # Convert history to agent format
    agent_messages = [
        {"role": msg.role.value, "content": msg.content}
        for msg in history
    ]
    agent_messages.append({"role": "user", "content": request.message})
    
    # Step 5: Run OpenAI Agent with MCP tools (Section 8.5)
    assistant_response, tool_calls = await run_agent(agent_messages)
    
    # Step 6: Persist assistant response and tool call metadata
    assistant_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role=MessageRole.ASSISTANT,
        content=assistant_response,
        created_at=datetime.utcnow()
    )
    db.add(assistant_message)
    
    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    db.add(conversation)
    db.commit()
    
    # Step 7: Return conversation_id, response, and tool_calls
    # Step 8: Discard all in-memory state (automatic - no globals/cache)
    return ChatResponse(
        conversation_id=conversation.id,
        response=assistant_response,
        tool_calls=tool_calls  # Transparency per Section 1.3
    )
