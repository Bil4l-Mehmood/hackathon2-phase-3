"""
Phase III Todo AI Chatbot - Main Application Entry Point.
Implements Section 2.1: High-Level Flow

FastAPI application with:
- Stateless chat endpoint (Section 8.6)
- Database initialization (Section 3)
- OpenAI Agent integration (Section 8.5)
- MCP tools (Section 4)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .db import create_db_and_tables
from .api import chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables on startup"""
    create_db_and_tables()
    yield


app = FastAPI(
    title="Phase III: Todo AI Chatbot",
    description="AI-powered conversational Todo management system (Agentic Dev Stack)",
    version="3.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat router per Section 8.6
# Note: user_id is a path parameter in the route itself
app.include_router(chat_router, tags=["chat"])


@app.get("/")
async def root():
    return {
        "message": "Phase III: Todo AI Chatbot API",
        "version": "3.0.0",
        "architecture": "Agentic Dev Stack (OpenAI + MCP)",
        "endpoints": {
            "chat": "POST /api/{user_id}/chat"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "ok", "mode": "stateless"}
