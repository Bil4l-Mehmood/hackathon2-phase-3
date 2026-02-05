# Phase III: Todo AI Chatbot

## Overview
An AI-powered chatbot for managing tasks via natural language. Uses a stateless agent architecture with a PostgreSQL database.

## Architecture
- **Frontend**: Next.js Chat Interface (Port 3001)
- **Backend**: FastAPI Agent Server (Port 8001)
- **AI Engine**: Cohere Command-R (via `cohere` SDK)
- **Database**: PostgreSQL (via SQLModel)

## Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL database
- Cohere API Key

### Backend Setup
1. Navigate to `backend/`:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure `.env`:
   ```
   DATABASE_URL=postgresql://user:pass@localhost/dbname
   COHERE_API_KEY=your_cohere_key
   ```
4. Run server:
   ```bash
   uvicorn src.main:app --reload --port 8001
   ```

### Frontend Setup
1. Navigate to `frontend/`:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Configure `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8001
   NEXT_PUBLIC_USER_ID=test-user-123
   ```
4. Run server:
   ```bash
   npm run dev -- -p 3001
   ```

## Usage
Open `http://localhost:3001` and chat with the assistant.
- "Add a task to buy milk"
- "List my tasks"
- "Complete task 1"

## Project Structure
- `src/api`: REST Endpoints
- `src/agent`: AI Logic (Cohere Runner)
- `src/mcp`: Tool definitions (simulated MCP)
- `specs/`: Project specifications
