# ExpenseDesk

An offline AI-powered expense management assistant. Ask questions about your company's expenses in plain English — ExpenseDesk generates the SQL, executes it safely, and returns a human-readable answer. No internet required after setup.

![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)
![SCSS](https://img.shields.io/badge/SCSS-CC6699?style=flat&logo=sass&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat&logo=ollama&logoColor=white)

---

## Table of Contents

- [What it does](#what-it-does)
- [Architecture](#architecture)
- [Agents](#agents)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [Monorepo Structure](#monorepo-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running locally](#running-locally-development)
- [Running with Kubernetes](#running-with-kubernetes)
- [API](#api)
- [Example queries](#example-queries)
- [Key design decisions](#key-design-decisions)
- [Kubernetes pod map](#kubernetes-pod-map)
- [License](#license)

---

## What it does

Type a question like _"Show me all pending expenses over $500 from the engineering team"_ and ExpenseDesk:

1. Retrieves relevant SQL examples from a local vector store (RAG)
2. Generates the correct SQL query using a local LLM
3. Executes the query safely via an MCP server
4. Summarizes the results in plain English
5. Displays both the answer and the raw SQL in the chat UI

Everything runs on your machine. No API keys. No cloud. No data leaves your network.

---

## Architecture

```
User question
      ↓
React frontend (Vite + TypeScript)
      ↓
FastAPI backend (/chat endpoint)
      ↓
┌─────────────────────────────────────┐
│  RAG Layer                          │
│  sqlite-vec + nomic-embed-text      │
│  retrieves top-3 similar SQL        │
│  examples from the SQL library      │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│  SQL Generation Agent               │
│  qwen2.5-coder:7b via Ollama        │
│  prompt = schema + RAG examples     │
│           + user question           │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│  MCP Server (Anthropic MCP SDK)     │
│  tools: list_tables                 │
│         get_schema                  │
│         execute_query               │
│  validates SQL before execution     │
│  rejects DROP, TRUNCATE, ALTER, DDL │
└─────────────────────────────────────┘
      ↓
SQLite database
      ↓
┌─────────────────────────────────────┐
│  Summarization Agent                │
│  llama3.1:8b via Ollama             │
│  translates rows → human answer     │
└─────────────────────────────────────┘
      ↓
Chat UI — answer + collapsible SQL panel
```

---

## Agents

ExpenseDesk uses two specialized AI agents:

### SQL Generation Agent
- **Model:** `qwen2.5-coder:7b`
- **Job:** Generates the correct SQL query from a natural language question
- **Tools:** `list_tables`, `get_schema`, `execute_query` via MCP
- **Prompt includes:** Live schema from MCP + top-3 RAG examples + user question
- **Temperature:** 0 (deterministic output)
- **Output:** SQL only — no explanation

### Summarization Agent
- **Model:** `llama3.1:8b`
- **Job:** Translates raw database rows into a human-readable answer
- **Tools:** None — pure language task
- **Input:** Original question + raw rows from the database
- **Output:** Natural language summary of the results

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + TypeScript + SCSS |
| Backend | Python + FastAPI |
| LLM Runtime | Ollama (fully local) |
| SQL Agent Model | qwen2.5-coder:7b |
| Summarization Model | llama3.1:8b |
| Embeddings | nomic-embed-text via Ollama |
| MCP Server | Python + Anthropic MCP SDK |
| Database | SQLite |
| Vector Store | SQLite + sqlite-vec extension |
| Containerization | Docker |
| Orchestration | Kubernetes (Docker Desktop) |

---

## Database Schema

```sql
employees    — id, name, department_id, role
departments  — id, name, manager_id
expenses     — id, employee_id, amount, category_id, status, date, description
categories   — id, name, budget_limit
vendors      — id, name, contact, payment_terms
approvals    — id, expense_id, approved_by, approved_at
```

---

## Monorepo Structure

```
ExpenseDesk/
├── frontend/                   React + Vite + TypeScript
│   ├── src/
│   │   ├── components/
│   │   │   ├── TopBar/
│   │   │   ├── Chat/
│   │   │   ├── Message/
│   │   │   └── InputBar/
│   │   └── styles/
│   │       ├── _variables.scss
│   │       ├── _themes.scss
│   │       └── global.scss
│   └── Dockerfile
├── backend/                    Python + FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── agents/
│   │   │   ├── sql_agent.py
│   │   │   └── summary_agent.py
│   │   └── rag/
│   │       └── retriever.py
│   └── requirements.txt
├── mcp-server/                 Anthropic MCP SDK
│   ├── server.py
│   └── requirements.txt
├── data/
│   ├── database.db             SQLite database
│   └── sql_examples.json       RAG example library
├── k8s/                        Kubernetes manifests
│   ├── frontend.yaml
│   ├── backend.yaml
│   ├── mcp-server.yaml
│   ├── ollama.yaml
│   ├── ollama-pvc.yaml
│   ├── sqlite-pvc.yaml
│   └── configmap.yaml
└── .env
```

---

## Prerequisites

- macOS (Apple Silicon recommended)
- Docker Desktop with Kubernetes enabled
- Python 3.11
- Node.js 20+
- Ollama

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/imarmang/ExpenseDesk.git
cd ExpenseDesk
```

### 2. Pull Ollama models

```bash
ollama pull qwen2.5-coder:7b
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

### 3. Set up the backend virtual environment

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Set up the MCP server virtual environment

```bash
cd mcp-server
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Install frontend dependencies

```bash
cd frontend
npm install
```

---

## Running locally (development)

Open four terminal tabs:

```bash
# Terminal 1 — Ollama
ollama serve

# Terminal 2 — MCP server
cd mcp-server && source venv/bin/activate
python server.py

# Terminal 3 — FastAPI backend
cd backend && source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 4 — React frontend
cd frontend
npm run dev
```

Open `http://localhost:5173`

---

## Running with Kubernetes

Make sure Docker Desktop is running with Kubernetes enabled.

```bash
# Build all images
docker build -t expensedesk-frontend:latest ./frontend
docker build -t expensedesk-backend:latest ./backend
docker build -t expensedesk-mcp:latest ./mcp-server

# Deploy the full stack
kubectl apply -f k8s/

# Verify all pods are running
kubectl get pods

# Open the app
open http://localhost:30000
```

To stop everything:

```bash
kubectl delete -f k8s/
```

---

## API

### `POST /chat`

Accepts a natural language question and returns a response with the SQL query and a human-readable answer.

**Request:**
```json
{
  "message": "Show me all pending expenses over $500 from the engineering team"
}
```

**Response:**
```json
{
  "response": "Found 3 pending expenses from Engineering over $500. Total outstanding is $2,340.",
  "sql": "SELECT e.id, emp.name, e.amount FROM expenses e JOIN employees emp ON e.employee_id = emp.id WHERE e.status = 'pending' AND e.amount > 500 ORDER BY e.amount DESC;"
}
```

Interactive API docs available at `http://localhost:8000/docs`

---

## Example queries

```
"Show me all pending expenses this month"
"Which employees have the most expenses?"
"What is the total spend by department this quarter?"
"Approve all of John Smith's pending expenses"
"Show me expenses over budget for the marketing category"
"List all vendors we paid more than $1,000 last month"
```

---

## Key design decisions

**Why offline?**
Company expense data is sensitive. Running entirely on-device means no data ever leaves the network — important for firms with compliance requirements or air-gapped environments.

**Why MCP for database access?**
The MCP server acts as a validation layer between the AI agent and the database. It rejects dangerous SQL (DROP, TRUNCATE, ALTER) before execution, so the agent never has raw database access.

**Why two agents?**
`qwen2.5-coder:7b` is optimized for code tasks and produces precise SQL. `llama3.1:8b` is optimized for natural language and produces better human-readable summaries. Splitting the responsibility gives better results than asking one model to do both.

**Why RAG for SQL generation?**
Without examples, the model has to guess your schema's exact table and column names. The RAG layer retrieves the most relevant SQL examples from your library and injects them as few-shot examples — dramatically improving SQL accuracy on your specific schema.

**Why Kubernetes?**
With four services (frontend, backend, MCP server, Ollama) running simultaneously, Kubernetes provides a single-command startup, automatic pod restarts on failure, and clean service-to-service communication via internal DNS — all without managing four separate terminal processes.

---

## Kubernetes pod map

```
Node: docker-desktop (local MacBook)
├── Pod: frontend     → Nginx serving React app  → localhost:30000
├── Pod: backend      → FastAPI                  → internal :8000
├── Pod: mcp-server   → MCP server               → internal :3000
└── Pod: ollama       → Ollama LLM runtime       → internal :11434
```

---

## License

This project is licensed under the [MIT License](LICENSE).