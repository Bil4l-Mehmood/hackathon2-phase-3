# Phase III Todo AI Chatbot - Frontend

OpenAI ChatKit-style interface for Todo AI Chatbot.

## Setup

Install dependencies:
```bash
npm install
```

## Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_USER_ID=test-user-123
```

## Run

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Architecture

- Next.js 15 + TypeScript + Tailwind CSS
- Chat interface inspired by ChatKit design patterns
- Stateless API calls to `POST /api/{user_id}/chat`
- Tool call transparency per Section 1.3
