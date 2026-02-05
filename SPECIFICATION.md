# Phase III: Todo AI Chatbot (Agentic Dev Stack)

> *Spec-Kit Plus Command Interface*
> 
>All lifecycle actions in this document can be executed or referenced using /sp.* commands.
> These commands are *conceptual orchestration commands* used for review, traceability, and Claude Code execution.
> 
>| Command            | Purpose                                                  |
> | ------------------ | -------------------------------------------------------- |
> | /sp.constitution | Load and lock Product Constitution                       |
> | /sp.spec         | Load system specifications (architecture, models, tools) |
> | /sp.plan         | Generate or review execution plan                        |
> | /sp.tasks        | Generate or review atomic task breakdown                 |
> | /sp.implement    | Execute Claude Code implementation prompts               |
> | /sp.acceptance   | Run acceptance checklist and validation                  |
> | /sp.remediate    | Handle errors via remediation playbook                   |

> *Spec-Kit Plus Traceability Index*
> 
>* *SP Constitution* → Section 1
> * *SP Specification* → Sections 2–5
> * *SP Plan* → Section 6
> * *SP Tasks* → Section 7
> * *SP Implementation* → Section 8
> * *SP Acceptance* → Sections 9–10

---

## 1. Product Constitution (Spec-Kit Plus)

*SP Command:* /sp.constitution

### 1.1 Objective

Deliver an AI-powered conversational Todo management system that allows authenticated users to manage tasks using natural language. The system must strictly follow an agentic workflow (spec → plan → tasks → implementation) and prohibit manual coding. All state must be persisted in Neon PostgreSQL, with stateless APIs and MCP tools.

### 1.2 Non-Negotiable Constraints

* No manual coding; all implementation via Claude Code.
* All AI logic must use OpenAI Agents SDK.
* Task operations must be exposed exclusively via MCP tools using the Official MCP SDK.
* APIs and MCP tools must be stateless; persistence handled by the database.
* Authentication enforced via Better Auth.
* Full auditability: prompts, plans, and iterations must be reviewable.

### 1.3 Success Criteria

* Users can add, list, update, complete, and delete tasks via natural language.
* Every user action maps to exactly one MCP tool invocation when applicable.
* Conversation state is persisted and recoverable.
* Tool calls are returned in the chat response for transparency.

---

## 2. System Architecture Specification

*SP Command:* /sp.spec

### 2.1 High-Level Flow

1. User sends a message from ChatKit UI.
2. FastAPI /api/{user_id}/chat endpoint receives request.
3. Conversation and message are persisted.
4. OpenAI Agent interprets intent.
5. Agent invokes MCP tools for task operations.
6. MCP server performs DB operation and returns result.
7. Agent generates a confirmation response.
8. Response, tool calls, and updated conversation ID are returned to frontend.

### 2.2 Statelessness Model

* Chat endpoint: no in-memory session state.
* MCP tools: pure functions + database access.
* Conversation continuity achieved by loading messages from DB.

---

## 3. Data Model Specification (SQLModel)

### Task

* id (int, PK)
* user_id (string, indexed)
* title (string)
* description (string, nullable)
* completed (bool, default false)
* created_at (datetime)
* updated_at (datetime)

### Conversation

* id (int, PK)
* user_id (string, indexed)
* created_at (datetime)
* updated_at (datetime)

### Message

* id (int, PK)
* conversation_id (FK)
* user_id (string)
* role (enum: user | assistant)
* content (text)
* created_at (datetime)

---

## 4. MCP Tool Contract (Authoritative)

### add_task

* Trigger: create/add/remember
* Input: user_id, title, description?
* Output: task_id, status=created, title

### list_tasks

* Trigger: list/show/see
* Input: user_id, status?
* Output: array of tasks

### complete_task

* Trigger: done/complete/finished
* Input: user_id, task_id
* Output: task_id, status=completed, title

### delete_task

* Trigger: delete/remove/cancel
* Input: user_id, task_id
* Output: task_id, status=deleted, title

### update_task

* Trigger: update/change/rename
* Input: user_id, task_id, title?, description?
* Output: task_id, status=updated, title

---

## 5. Agent Behavior Rules

1. Always infer intent before responding.
2. Never manipulate tasks directly; always call MCP tools.
3. If required parameters are missing, ask a clarifying question.
4. After every tool call, confirm the action in natural language.
5. On errors (e.g., task not found), respond politely and suggest next steps.

---

## 6. SP Plan – Execution Plan (Generated from Specification)

*SP Command:* /sp.plan

### Phase A: Foundation

* Initialize FastAPI backend with Better Auth middleware.
* Configure Neon PostgreSQL and SQLModel schemas.

### Phase B: MCP Server

* Initialize MCP server using Official MCP SDK.
* Implement all task tools with strict schema validation.

### Phase C: AI Agent

* Define agent instructions aligned with Behavior Rules.
* Register MCP tools with the agent.
* Implement runner to handle tool invocation and responses.

### Phase D: Chat API

* Implement /api/{user_id}/chat endpoint.
* Persist conversations and messages.
* Hydrate agent context from conversation history.

### Phase E: Frontend Integration

* Connect ChatKit UI to chat endpoint.
* Display assistant responses and tool calls.

---

## 7. SP Tasks – Atomic Task Breakdown (Reviewable)

*SP Command:* /sp.tasks

1. Create database models and migrations.
2. Implement MCP server bootstrap.
3. Implement add_task tool.
4. Implement list_tasks tool.
5. Implement complete_task tool.
6. Implement delete_task tool.
7. Implement update_task tool.
8. Configure OpenAI Agent with tools.
9. Implement stateless chat endpoint.
10. Integrate ChatKit frontend.
11. End-to-end testing with sample conversations.

---

## 8. SP Implementation – Claude Code Prompt Templates (Spec-Ready, Enforceable)

*SP Command:* /sp.implement

> These prompts are *authoritative*. They must be used verbatim in Claude Code. Any deviation constitutes manual coding and fails evaluation.

### 8.1 Master System Prompt (Agentic Enforcement)

"""
You are Claude Code operating under a strict Agentic Dev Stack workflow.

NON-NEGOTIABLE RULES:

* You MUST follow the provided specification as the single source of truth.
* You MUST NOT introduce features, logic, or shortcuts not explicitly defined.
* You MUST NOT write manual glue logic outside assigned tasks.
* All task mutations MUST occur exclusively through MCP tools.
* All APIs and MCP tools MUST be stateless.
* Persistence is allowed ONLY via the database layer.
* Every implementation step must be traceable to a spec section.

OUTPUT REQUIREMENTS:

* Generate production-ready code only for the requested task.
* Do not explain concepts unless explicitly asked.
* Do not refactor unrelated components.
"""

---

### 8.2 Database Models & Migration Prompt

"""
Implement SQLModel database schemas for Task, Conversation, and Message exactly as defined in Section 3 of the specification.

Requirements:

* Use SQLModel and PostgreSQL-compatible types.
* Include timestamps and indexes as specified.
* Ensure foreign key relationships are correctly enforced.
* Do not include business logic or API endpoints.
* Output only the model and migration-related code.
"""

---

### 8.3 MCP Server Bootstrap Prompt

"""
Initialize an MCP server using the Official MCP SDK.

Requirements:

* The MCP server must be stateless.
* Register tools without embedding business logic outside tool handlers.
* Use dependency injection for database access.
* Do not include FastAPI routes or agent logic.
* Prepare the server for tool registration only.
"""

---

### 8.4 MCP Tool Implementation Prompt (One Tool per Run)

"""
You are implementing an MCP tool using the Official MCP SDK.

Tool Name: {{tool_name}}

Specification:

* Inputs and outputs MUST match Section 4 exactly.
* Validate ownership using user_id.
* Persist state using SQLModel with Neon PostgreSQL.
* Return structured JSON only.
* Do not call other tools.
* Do not include logging, UI, or agent code.

Failure Conditions:

* Hidden state
* Multiple responsibilities
* Deviation from schema
"""

---

### 8.5 OpenAI Agent Configuration Prompt

"""
Define an OpenAI Agent using the OpenAI Agents SDK.

Agent Responsibilities:

* Interpret user intent from natural language.
* Select the correct MCP tool based on Section 7 command mapping.
* Never manipulate tasks directly.
* Ask clarifying questions when parameters are missing.
* Confirm every successful action in natural language.

Configuration Requirements:

* Register all MCP tools.
* Enable tool-call logging.
* Do not store memory in the agent.
"""

---

### 8.6 Stateless Chat Endpoint Prompt

"""
Implement a FastAPI POST endpoint: /api/{user_id}/chat

Execution Contract:

1. Accept message and optional conversation_id.
2. Fetch conversation history from the database.
3. Build agent message array (history + new message).
4. Persist the user message before agent execution.
5. Run the OpenAI Agent with MCP tools.
6. Persist assistant response and tool call metadata.
7. Return conversation_id, response text, and tool_calls.
8. Discard all in-memory state after response.

Constraints:

* Stateless per request.
* No global variables.
* No cached sessions.
"""

---

### 8.7 ChatKit Frontend Integration Prompt

"""
Integrate OpenAI ChatKit with the /api/{user_id}/chat endpoint.

Requirements:

* Send user messages as stateless requests.
* Display assistant responses verbatim.
* Render tool call summaries for transparency.
* Do not implement client-side state beyond UI rendering.
"""

---

## 8.8 ChatKit Setup & Deployment (Hosted Mode – Required)

### Domain Allowlist Configuration

Before deploying the chatbot frontend, configure OpenAI's *Domain Allowlist* to enable hosted ChatKit securely.

Deployment prerequisites:

* Deploy the frontend to obtain a production URL:
  * Vercel: https://your-app.vercel.app
  * GitHub Pages: https://username.github.io/repo-name
  * Custom Domain: https://yourdomain.com

Allowlist steps:

1. Navigate to OpenAI Organization Settings → Security → Domain Allowlist
2. Click *Add domain*
3. Enter the frontend URL *without trailing slash*
4. Save changes

After allowlisting:

* Obtain the *ChatKit Domain Key* issued by OpenAI
* Use this key in the frontend runtime configuration

### Environment Variables

NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here

### Development Note

* Hosted ChatKit requires allowlisted domains
* Local development (localhost) typically works without allowlisting

---

### 8.8.1 ChatKit Deployment Execution Prompt (Spec-Kit Plus)

"""
You are executing the ChatKit Hosted Deployment step for the Phase III Todo AI Chatbot.

Objectives:

* Validate that the frontend is deployed to a public HTTPS URL.
* Confirm that the deployment domain is added to the OpenAI Domain Allowlist.
* Verify that a valid ChatKit Domain Key has been issued.
* Ensure the domain key is injected via NEXT_PUBLIC_OPENAI_DOMAIN_KEY.

Validation Steps:

1. Inspect frontend deployment configuration and confirm production URL.
2. Verify domain presence in OpenAI Organization → Security → Domain Allowlist.
3. Confirm ChatKit Domain Key exists and matches the allowlisted domain.
4. Verify frontend runtime has access to NEXT_PUBLIC_OPENAI_DOMAIN_KEY.
5. Perform a hosted ChatKit request and confirm successful connection.

Output Requirements:

* Deployment validation report
* PASS/FAIL for each validation step
* Reference Section 8.8 for all checks

Constraints:

* Do not modify frontend or backend code.
* Do not bypass domain allowlist requirements.
"""

---

## 9. SP Acceptance Checklist (Functional & Review)

*SP Command:* /sp.acceptance

> This checklist defines *what must be validated*. The executable prompt that operationalizes this checklist is provided below.

### 9.1 Acceptance Criteria

* [ ] All CRUD todo operations work via natural language only
* [ ] Each user intent maps to the correct MCP tool
* [ ] Ambiguous references resolve via list_tasks before mutation
* [ ] MCP tools are stateless and database-backed
* [ ] Chat API is stateless per request
* [ ] Conversation and message history persist correctly
* [ ] Tool calls are returned in chat responses
* [ ] Authentication enforced for all operations
* [ ] No manual code written outside Claude Code runs

---

### 9.2 Acceptance Checklist Execution Prompt (Spec-Kit Plus)

"""
You are executing the *SP Acceptance Checklist* for the Phase III Todo AI Chatbot.

Instructions:

* Treat each checklist item as a mandatory acceptance test.
* Do not modify code or configuration.
* Use simulated chat requests where needed.
* Inspect tool calls, database state, and API responses.

For each acceptance item:

1. Describe the validation step performed.
2. Mark the result as PASS or FAIL.
3. Reference the exact spec section (by number).

Output Format:

* Checklist table
* One row per acceptance item
* Columns: Acceptance Item | Validation Method | Result | Spec Reference

Constraints:

* Do not introduce new tests beyond the checklist.
* Do not skip any acceptance item.
"""

---

## 10. Acceptance Validation Prompt (Judge-Ready)

> Use this prompt as the *final Claude Code run* to self-validate the Todo AI Chatbot.

"""
You are acting as a strict evaluator validating the Phase III Todo AI Chatbot against its specification.

Validation Tasks:

1. Simulate user conversations for add, list, update, complete, and delete operations.
2. Verify that each operation invokes the correct MCP tool.
3. Confirm that ambiguous task references trigger list_tasks before mutation.
4. Inspect that no in-memory state is retained between requests.
5. Validate that conversation and message records persist correctly in the database.
6. Ensure tool calls are included in the API response payload.

Output Requirements:

* Produce a checklist-style validation report.
* Mark each acceptance criterion as PASS or FAIL.
* Reference the relevant spec section for each check.
* Do not modify any code.
"""

---

## 11. SP Error Handling & Remediation Playbook (Mandatory)

*SP Command:* /sp.remediate

This section defines *what to do when errors occur*, without violating the Agentic Dev Stack rules or introducing manual fixes.

### 11.1 Error Classification

Classify every issue into *exactly one* category:

* *Spec Error*: Ambiguity, contradiction, or missing requirement in Sections 1–5
* *Plan Error*: Incorrect sequencing or missing phase in Section 6
* *Task Error*: Task granularity or order issue in Section 7
* *Implementation Error*: Bug or mismatch produced by Claude Code in Section 8
* *Acceptance Error*: Failure against Section 9 checklist

---

### 11.2 Mandatory Response Protocol (No Manual Coding)

When any error is detected:

1. *Stop implementation immediately*.
2. Identify the error category (11.1).
3. Locate the *exact spec section* violated.
4. Do *not* patch code manually.
5. Run the appropriate Claude Code remediation prompt (below).
6. Commit the fix with a message referencing the spec section.

---

### 11.3 Claude Code Remediation Prompts

#### A. Spec Clarification Prompt (Spec Error)

"""
You are reviewing the Phase III specification.

Task:

* Identify ambiguity or inconsistency in the referenced section.
* Propose a minimal clarification that preserves existing intent.
* Do not introduce new features.
* Output only the revised spec text.
"""

---

#### B. Plan Correction Prompt (Plan Error)

"""
Review the SP Plan (Section 6).

Task:

* Identify the incorrect or missing step.
* Generate a corrected execution plan.
* Do not modify tasks or implementation.
"""

---

#### C. Task Repair Prompt (Task Error)

"""
Review SP Tasks (Section 7).

Task:

* Identify task ordering or granularity issues.
* Split or reorder tasks if required.
* Preserve task intent.
"""

---

#### D. Implementation Fix Prompt (Implementation Error)

"""
You are fixing an implementation error generated by Claude Code.

Constraints:

* Reference the exact failing spec section.
* Regenerate only the affected component.
* Do not refactor unrelated files.
* Maintain statelessness and MCP-only mutations.
"""

---

#### E. Acceptance Failure Prompt (Acceptance Error)

"""
An acceptance criterion has FAILED.

Task:

* Identify the root cause.
* Map it to Spec, Plan, Task, or Implementation.
* Generate the minimal corrective change.
* Do not bypass acceptance rules.
"""

---

### 11.4 Error Evidence Log (Required for Review)

For every error, record:

* Error category
* Failing acceptance item or spec section
* Claude Code prompt used
* Files regenerated
* Commit hash

---

Following this playbook is mandatory. Manual hotfixes invalidate the submission.

---

## 12. Key Architecture Benefits (Informational)

| Aspect               | Benefit                                                  |
| -------------------- | -------------------------------------------------------- |
| MCP Tools            | Standardized interface for AI-to-application interaction |
| Single Chat Endpoint | Simplified API surface; agent routes to tools            |
| Stateless Server     | Horizontally scalable and resilient                      |
| Tool Composition     | Agent can chain multiple tools in a single turn          |

---

This document is the single source of truth for Phase III implementation and review.
