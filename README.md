# 🤖 QA AI Assistant

An end-to-end **AI-powered QA engineering assistant** built with Python,
FastAPI, Ollama/Llama 3.2, RAG, embeddings, ChromaDB, SQLite, Pytest,
Docker, and GitHub Actions.

The project demonstrates how Generative AI can be integrated into a
practical software testing workflow --- from requirement analysis and
test-case generation to API/UI testing, failure analysis, evaluation,
containerization, and CI/CD.

------------------------------------------------------------------------

## 🚀 What this project does

The QA AI Assistant provides a web-based interface and REST APIs that
can:

-   Answer QA/testing questions using an LLM
-   Maintain conversation history using SQLite
-   Upload and ingest QA documentation
-   Chunk documents into searchable pieces
-   Generate embeddings using `nomic-embed-text`
-   Store and retrieve vectors using ChromaDB
-   Use Retrieval-Augmented Generation (RAG) to ground answers in
    documentation
-   Analyze software requirements
-   Generate structured test cases
-   Validate generated test cases
-   Generate and execute API tests
-   Generate and execute UI tests
-   Analyze test failures
-   Run AI-driven QA agent workflows
-   Evaluate AI-generated outputs
-   Run automated Pytest validation
-   Run inside Docker
-   Automatically validate changes through GitHub Actions CI/CD

------------------------------------------------------------------------

# 🏗️ High-Level Architecture

``` text
                    ┌───────────────────────────┐
                    │        User / QA          │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │        Web UI              │
                    │     HTML / CSS / JS        │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │        FastAPI             │
                    │       REST APIs            │
                    └─────────────┬─────────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      ┌─────────────┐     ┌──────────────┐     ┌──────────────┐
      │ Requirement │     │ Test Case    │     │ API / UI     │
      │  Analysis   │     │ Generation   │     │ Testing      │
      └─────────────┘     └──────────────┘     └──────────────┘
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  ▼
                    ┌───────────────────────────┐
                    │     RAG Pipeline           │
                    │                           │
                    │ Document → Chunk → Embed  │
                    │ → ChromaDB → Retrieve     │
                    │ → LLM → Grounded Answer   │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │     Ollama / Llama 3.2    │
                    │       Local LLM           │
                    └───────────────────────────┘

Supporting infrastructure:

        SQLite ──► conversation persistence
        Pytest ──► automated validation
        Docker ──► containerization
        GitHub Actions ──► CI/CD
```

------------------------------------------------------------------------

# 🧠 RAG Architecture

The project uses Retrieval-Augmented Generation rather than asking the
LLM to answer from general knowledge alone.

``` text
QA Documentation
      │
      ▼
Document Ingestion
      │
      ▼
Text Extraction
      │
      ▼
Chunking
      │
      ▼
Embedding Model
(nomic-embed-text)
      │
      ▼
ChromaDB
(Vector Database)
      │
      │
User Question
      │
      ▼
Question Embedding
      │
      ▼
Semantic Search
      │
      ▼
Relevant Chunks
      │
      ▼
Context + Question
      │
      ▼
Llama 3.2
      │
      ▼
Grounded Answer
```

### Why RAG?

A normal LLM can generate plausible answers even when it does not know
the application's actual requirements.

RAG reduces this problem by retrieving relevant project documentation
and providing it to the LLM as context.

The assistant is instructed to:

1.  Prefer provided documentation.
2.  Avoid inventing requirements.
3.  Clearly state when information is unavailable.
4.  Use conversation history when relevant.

------------------------------------------------------------------------

# 📚 Knowledge Base

The assistant supports document-based knowledge ingestion.

Example requirement:

``` text
After 5 consecutive failed login attempts,
the user account will be locked.

The account will remain locked for 15 minutes.
```

A user can ask:

``` text
What happens after 5 failed login attempts?
```

The system retrieves the relevant documentation and generates a grounded
answer.

------------------------------------------------------------------------

# 🧪 AI QA Capabilities

## 1. Requirement Analysis

The assistant can analyze requirements and identify:

-   Functional expectations
-   Missing information
-   Ambiguities
-   Positive scenarios
-   Negative scenarios
-   Boundary conditions
-   Risks
-   Testing considerations

------------------------------------------------------------------------

## 2. Test Case Generation

The assistant generates structured test cases containing information
such as:

``` text
Test Case ID
Requirement ID
Requirement
Scenario
Test Type
Priority
Risk
Preconditions
Test Steps
Test Data
Expected Result
Traceability
```

Example test types:

-   Positive
-   Negative
-   Boundary
-   Edge case
-   Functional
-   Regression

------------------------------------------------------------------------

## 3. Test Case Validation

Generated test cases are validated before being treated as usable
output.

The validator checks the expected structure and required fields.

Example:

``` text
Validation result:
{
    "valid": true,
    "errors": []
}
```

------------------------------------------------------------------------

## 4. API Testing

The project can generate and execute API-oriented tests.

The workflow can include:

``` text
API Description
      ↓
AI Test Generation
      ↓
Generated API Tests
      ↓
Execution
      ↓
Response Validation
      ↓
Result
```

------------------------------------------------------------------------

## 5. UI Testing

The project includes UI testing capabilities and can generate browser
automation-oriented tests.

The goal is to demonstrate AI-assisted test creation rather than
replacing traditional automation frameworks.

------------------------------------------------------------------------

## 6. Failure Analysis

The assistant can analyze failed test information and provide:

-   Likely cause
-   Failure interpretation
-   Possible root cause
-   Recommended investigation
-   Suggested next QA action

------------------------------------------------------------------------

## 7. AI QA Agent

The project includes an AI QA agent workflow that can coordinate
QA-related capabilities rather than treating the LLM as only a
question-answering chatbot.

Conceptually:

``` text
User Goal
   ↓
AI QA Agent
   ↓
Choose appropriate QA capability
   ├── Requirement Analysis
   ├── Test Generation
   ├── API Testing
   ├── UI Testing
   └── Failure Analysis
```

------------------------------------------------------------------------

# 💾 Conversation Memory

Conversation history is persisted using SQLite.

``` text
Browser
   ↓
Session ID
   ↓
FastAPI
   ↓
SQLite
   ↓
Conversation History
```

This allows the assistant to maintain context across requests.

For example:

``` text
User:
What happens after 5 failed login attempts?

AI:
The account is locked.

User:
For how long?

AI:
15 minutes.
```

------------------------------------------------------------------------

# 🗄️ Vector Database

The project initially used a JSON file for embeddings during
development.

It was then upgraded to **ChromaDB**.

This demonstrates an important architectural evolution:

``` text
Initial prototype
-----------------
embeddings.json
       ↓
manual cosine similarity


Production-oriented prototype
-----------------------------
ChromaDB
       ↓
vector retrieval
```

This makes the vector retrieval layer easier to scale and maintain.

------------------------------------------------------------------------

# 🛠️ Technology Stack

  Technology            Purpose
  --------------------- ---------------------------
  Python                Core application
  FastAPI               REST API/backend
  HTML/CSS/JavaScript   Web UI
  Ollama                Local LLM runtime
  Llama 3.2             Local language model
  nomic-embed-text      Embeddings
  ChromaDB              Vector database
  SQLite                Conversation persistence
  Pytest                Automated testing
  Playwright            UI automation capability
  Docker                Containerization
  Git                   Version control
  GitHub                Source control
  GitHub Actions        CI/CD
  python-dotenv         Environment configuration

------------------------------------------------------------------------

# 📁 Project Structure

``` text
qa-ai-assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── db.py
│   ├── prompts.py
│   │
│   ├── ingest.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── build_embeddings.py
│   ├── search.py
│   │
│   ├── vector_store.py
│   ├── index_vectors.py
│   ├── vector_search.py
│   │
│   ├── rag.py
│   ├── pdf_loader.py
│   │
│   ├── test_case_validator.py
│   ├── test_generator.py
│   ├── api_test_generator.py
│   ├── api_test_runner.py
│   ├── api_testing.py
│   │
│   ├── evaluator.py
│   ├── agent.py
│   ├── config.py
│   └── security.py
│
├── knowledge/
│   └── QA requirement documents
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── tests/
│   └── automated Pytest tests
│
├── data/
│   ├── chatbot.db
│   └── chroma_db/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

# ⚙️ Local Setup

## 1. Clone the repository

``` powershell
git clone https://github.com/govindkumit/qa-ai-assistant.git
cd qa-ai-assistant
```

## 2. Create a virtual environment

``` powershell
python -m venv .venv
```

Activate it:

``` powershell
.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

``` powershell
pip install -r requirements.txt
```

## 4. Install Ollama

Install Ollama separately and make sure it is running.

Pull the required models:

``` powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

Verify:

``` powershell
ollama list
```

------------------------------------------------------------------------

# ▶️ Run the Application

From the project root:

``` powershell
uvicorn app.main:app --reload
```

Open:

``` text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# 🧪 Run Tests

Run the complete test suite:

``` powershell
pytest -q
```

Expected result in the completed project:

``` text
5 passed
```

------------------------------------------------------------------------

# 🐳 Docker

Build the image:

``` powershell
docker build -t qa-ai-assistant .
```

Run the container:

``` powershell
docker run -p 8000:8000 qa-ai-assistant
```

Verify:

``` powershell
docker ps
```

Open:

``` text
http://localhost:8000
```

------------------------------------------------------------------------

# 🔄 CI/CD

GitHub Actions automatically validates changes pushed to the repository.

``` text
Developer
   │
   │ git push
   ▼
GitHub
   │
   ▼
GitHub Actions
   │
   ├── Install dependencies
   ├── Run automated tests
   └── Validate build
   │
   ▼
    ✅ PASS
```

The repository contains:

``` text
.github/workflows/ci.yml
```

The CI pipeline has been successfully executed against the project.

------------------------------------------------------------------------

# 🔌 Important API Endpoints

The FastAPI application exposes endpoints for major QA capabilities,
including:

  Endpoint                      Purpose
  ----------------------------- ---------------------------------
  `POST /chat`                  General QA assistant / RAG chat
  `POST /upload`                Upload knowledge documents
  `POST /analyze-requirement`   Analyze requirements
  `POST /generate-test-cases`   Generate test cases
  `POST /api-test`              API testing workflow
  `POST /ui-test`               UI testing workflow
  `POST /analyze-failure`       Failure analysis
  `POST /agent`                 AI QA agent workflow
  `GET /docs`                   Swagger API documentation

The exact request/response schemas can be explored interactively through
FastAPI Swagger.

------------------------------------------------------------------------

# 🔐 Security Considerations

This project is designed as a learning and portfolio application.

Before production deployment, the following should be strengthened:

-   Authentication and authorization
-   Session ownership validation
-   Secure secret management
-   Input validation
-   Output sanitization
-   XSS protection
-   Rate limiting
-   File upload restrictions
-   File size limits
-   Malware scanning
-   API authentication
-   Audit logging
-   HTTPS
-   Production database configuration
-   Secure Docker configuration
-   Observability and monitoring

The current implementation should therefore be viewed as a
**portfolio/reference architecture**, not a production security
baseline.

------------------------------------------------------------------------

# 📈 Evolution of the Project

The project was developed incrementally.

``` text
V1
Python + Ollama + Llama
        ↓
V2
Conversation Memory
        ↓
V3
QA System Prompt
        ↓
V4
FastAPI + Web UI
        ↓
V5
SQLite Persistent Memory
        ↓
V6
RAG Pipeline
        ↓
Document Ingestion
        ↓
Chunking
        ↓
Embeddings
        ↓
Semantic Search
        ↓
RAG Generation
        ↓
ChromaDB
        ↓
V7/V8
Document & QA capabilities
        ↓
Requirement Analysis
        ↓
Test Case Generation
        ↓
Test Case Validation
        ↓
API Testing
        ↓
UI Testing
        ↓
Failure Analysis
        ↓
V9+
AI QA Agent + Evaluation
        ↓
Configuration + Security
        ↓
Pytest
        ↓
Docker
        ↓
GitHub
        ↓
GitHub Actions CI/CD
```

------------------------------------------------------------------------

# 🎯 Why this project is relevant to AI QA roles

This project demonstrates practical experience across both **QA
engineering and Generative AI**.

### QA Engineering

-   Requirement analysis
-   Test design
-   Functional testing
-   Negative testing
-   Boundary testing
-   API testing
-   UI testing
-   Automation
-   Failure analysis
-   Test validation
-   Regression-oriented thinking

### AI Engineering

-   LLM integration
-   Prompt engineering
-   Conversation memory
-   Embeddings
-   Vector databases
-   Semantic retrieval
-   RAG
-   Grounding
-   AI evaluation
-   AI agents
-   Local LLM deployment

### Engineering / DevOps

-   Python
-   FastAPI
-   REST APIs
-   SQLite
-   Docker
-   Git
-   GitHub
-   GitHub Actions
-   CI/CD
-   Automated testing

------------------------------------------------------------------------

# 🧑‍💻 Resume Project Description

A concise resume version:

> **AI-Powered QA Assistant** --- Built an end-to-end AI QA platform
> using Python, FastAPI, Ollama/Llama 3.2, RAG, embeddings, ChromaDB,
> and SQLite. Implemented requirement analysis, structured test-case
> generation and validation, API/UI testing, failure analysis, and an AI
> QA agent workflow. Containerized the application with Docker and
> implemented GitHub Actions CI/CD with automated Pytest validation.

------------------------------------------------------------------------

# 🗣️ Interview Explanation

A strong short explanation:

> "I built this project to understand how Generative AI can be applied
> to real QA engineering workflows. I started with a local LLM using
> Ollama and gradually added conversation memory, FastAPI, document
> ingestion, embeddings, semantic retrieval and RAG. I then moved the
> vector layer to ChromaDB and added QA-specific capabilities such as
> requirement analysis, structured test-case generation, validation,
> API/UI testing and failure analysis. Finally, I added automated
> evaluation and Pytest validation, containerized the application with
> Docker, and implemented GitHub Actions CI/CD. The key architectural
> principle was to keep the LLM grounded in project documentation rather
> than relying only on its general knowledge."

------------------------------------------------------------------------

# ⚠️ Current Project Scope

This project intentionally uses local AI components:

``` text
Ollama
  +
Llama 3.2
  +
nomic-embed-text
```

This avoids dependency on paid cloud LLM APIs during development and
makes the project easy to experiment with locally.

For production, the LLM and embedding layer could be replaced with
managed or self-hosted enterprise models.

------------------------------------------------------------------------

# 🔮 Potential Production Enhancements

Future improvements could include:

-   Authentication / RBAC
-   PostgreSQL
-   Redis
-   Background processing
-   Advanced document parsers
-   Reranking
-   Hybrid search
-   Better citation handling
-   LLM-as-a-judge evaluation
-   OpenTelemetry
-   Prometheus/Grafana
-   Cloud deployment
-   Kubernetes
-   Model gateway
-   Prompt/version management
-   Security scanning
-   Human approval workflows
-   Test result dashboards

These are intentionally outside the current MVP so the core project
remains understandable and maintainable.

------------------------------------------------------------------------

# 📌 Project Status

**Status: Completed ✅**

Core capabilities implemented:

-   AI assistant ✅
-   RAG ✅
-   ChromaDB ✅
-   Document ingestion ✅
-   QA requirement analysis ✅
-   Test-case generation ✅
-   Test-case validation ✅
-   API testing ✅
-   UI testing ✅
-   Failure analysis ✅
-   AI QA agent ✅
-   Evaluation ✅
-   Pytest ✅
-   Docker ✅
-   GitHub Actions CI/CD ✅

------------------------------------------------------------------------

## ⭐ Portfolio Goal

This repository demonstrates an end-to-end approach to building an
**AI-enabled QA engineering platform**, combining traditional software
testing practices with modern LLM, RAG, vector database, automation, and
DevOps techniques.
