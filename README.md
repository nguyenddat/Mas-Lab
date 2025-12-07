# MAS Lab: AI Agentic Workflow

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard-green)](https://github.com/modelcontextprotocol)

**MAS Lab** (Multi-Agent System Laboratory) is a monorepo designed to demonstrate advanced AI agentic workflows. It uniquely combines a robust **core platform** (Backend, MCP, DB) with a flexible **agent layer**, enabling the development and execution of autonomous agents that can interact with complex tools and data.

## 🚀 Key Features

### Core Infrastructure
-   **FastAPI Backend**: The central nervous system, managing data persistence, business logic, and API orchestration.
-   **MCP Server**: A dedicated Model Context Protocol (FastMCP) service that acts as a tool bridge, empowering agents with capabilities like:
    -   🔍 **Arxiv Search**: Query scientific papers directly.
    -   📝 **Paper Management**: Create, retrieve, and organize research papers.
-   **PostgreSQL Persistence**: Reliable relational database storage for application state.

### Agent Layer
-   **Agent Runners Service**: A specialized FastAPI service designed to host and execute autonomous agents (e.g., `AgentPaperCrawler`). It manages agent life cycles and handles incoming task requests.
-   **Standalone Agents**: Python scripts (like `agent.py`) demonstrating how to connect directly to the MCP server for ad-hoc tasks.

## 🏗️ Architecture

The project is composed of containerized core services and a local agent execution environment.

| Service | Type | Port | Description |
| :--- | :--- | :--- | :--- |
| **Backend** | Docker | `8000` | Core API & Business Logic (`lab_backend`) |
| **MCP Server** | Docker | `8001` | SSE-based Tool Server (`lab_mcp`) |
| **Database** | Docker | `5432` | PostgreSQL 15 (`lab_db`) |
| **Agent Runners** | Local | `8002` | Agent Execution Environment |

## � Technology Stack

### Backend Layer
*   **Framework**: `FastAPI` (High-performance async API)
*   **Database ORM**: `SQLAlchemy 2.0` (Modern Python ORM)
*   **Validation**: `Pydantic v2` (Robust data validation)
*   **Database**: `PostgreSQL 15` (Reliable relational storage)

### MCP Server Layer
*   **Protocol**: `Model Context Protocol (MCP)` (Standard for AI context exchange)
*   **Transport**: `SSE` (Server-Sent Events) for real-time tool stream
*   **Integration**: `arxiv` (Python wrapper for scientific paper access)

### Agent Layer
*   **LLM Integration**: `OpenAI API` (GPT-4o/GPT-3.5)
*   **Tooling**: `mcp` (Official Python client SDK)
*   **Runtime**: `AsyncIO` (Concurrent execution for responsive agents)

## �🛠️ Prerequisites

-   [Docker Desktop](https://www.docker.com/products/docker-desktop)
-   [Docker Compose](https://docs.docker.com/compose/install/)
-   **Python 3.10+** (For running agents locally)

## 🏁 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd mas-lab
```

### 2. Environment Configuration

Ensure `.env` files are configured in the respective directories:
*   `backend/.env`
*   `mcp/.env`
*   `database/.env`
*   `agent_runners/.env`

### 3. Start Core Infrastructure

Run the backend, MCP server, and database using Docker Compose:

```bash
docker-compose up --build
```
*   **Backend**: [http://localhost:8000](http://localhost:8000)
*   **MCP Server**: [http://localhost:8001](http://localhost:8001)

### 4. Start Agent Runners

The agent runner service is designed to run locally for easier development and debugging of agents.

```bash
cd agent_runners
# Install dependencies (ensure requirements are met)
pip install -r requirements.txt # (If verified) or install necessary packages manually
uvicorn main:app --host localhost --port 8002 --reload
```
*   **Agent Runners API**: [http://localhost:8002](http://localhost:8002)

## 📂 Project Structure

```
.
├── backend/                 # [Core] FastAPI Application
│   ├── core/               # App config & dependencies
│   ├── routers/            # API Endpoints
│   ├── services/           # Business logic
│   └── main.py             # App entry point
│
├── mcp/                     # [Core] Model Context Protocol Server
│   ├── tools/              # Agent Tools (e.g., Arxiv search)
│   └── main.py             # Server entry point
│
├── database/                # [Core] Database configuration
│
├── agent_runners/           # [Agent Layer] Agent Execution Service
│   ├── agents/             # Agent implementations (e.g., PaperCrawler)
│   ├── core/               # Agent framework core
│   └── main.py             # Runner service entry point
│
├── agent.py                 # [Example] Standalone agent script
└── docker-compose.yml       # Service orchestration
```

## 🔌 API Documentation

Explore the interactive documentation for each service:

-   **Backend API**: [http://localhost:8000/docs](http://localhost:8000/docs)
-   **Agent Runners API**: [http://localhost:8002/docs](http://localhost:8002/docs)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
