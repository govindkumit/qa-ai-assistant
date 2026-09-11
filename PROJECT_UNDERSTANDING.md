# QA AI Assistant --- Complete Project Understanding

This document explains the project from the beginning to the final
implementation in simple terms.

------------------------------------------------------------------------

# 1. The original goal

The goal was to build a real project that demonstrates:

-   Python
-   AI / LLM
-   QA engineering
-   RAG
-   Test automation
-   API testing
-   UI testing
-   AI agents
-   Docker
-   CI/CD
-   Git/GitHub

Instead of learning each technology separately, we built one application
and added capabilities step by step.

The final application is a local **QA AI Assistant**.

------------------------------------------------------------------------

# 2. V1 --- Connect Python to a local LLM

The first version connected Python to Ollama and the local Llama 3.2
model.

Concept:

``` text
Python
   ↓
Ollama
   ↓
Llama 3.2
   ↓
AI Response
```

Why Ollama?

Because it allowed the project to use a local model without depending on
a paid cloud API.

------------------------------------------------------------------------

# 3. V2 --- Conversation memory

A basic LLM call does not automatically know the previous conversation.

We introduced a Python `messages` list.

``` text
User question
     ↓
Conversation history
     ↓
LLM
     ↓
Answer
```

This allowed follow-up questions to use previous context.

------------------------------------------------------------------------

# 4. V3 --- QA-specific system prompt

We created a system prompt telling the model that it is a QA AI
Assistant.

The prompt established behavior such as:

-   Understand requirements first
-   Do not invent requirements
-   Generate positive and negative scenarios
-   Consider boundaries and edge cases
-   Produce maintainable automation code
-   Use meaningful assertions
-   Explain assumptions

This is the first important AI engineering concept in the project:

**Prompt engineering controls the role and behavior of the model.**

------------------------------------------------------------------------

# 5. V4 --- FastAPI and Web UI

The project was converted from a command-line application into a web
application.

Architecture:

``` text
Browser
   ↓
FastAPI
   ↓
Python
   ↓
Ollama
   ↓
Llama
```

FastAPI provided REST endpoints.

HTML/CSS/JavaScript provided the browser interface.

------------------------------------------------------------------------

# 6. V5 --- Persistent conversation memory

Python memory disappears when the application restarts.

We introduced SQLite.

``` text
Browser
   ↓
Session ID
   ↓
FastAPI
   ↓
SQLite
```

SQLite stores:

-   Sessions
-   User messages
-   Assistant messages

This introduced persistent application state.

------------------------------------------------------------------------

# 7. V6 --- RAG

This was one of the most important stages.

Problem:

An LLM may answer using general knowledge instead of the application's
real requirements.

Solution:

**Retrieval-Augmented Generation.**

The process became:

``` text
Documentation
     ↓
Chunking
     ↓
Embeddings
     ↓
Vector Store
     ↓
Retrieve relevant content
     ↓
Give retrieved content to LLM
     ↓
Grounded answer
```

------------------------------------------------------------------------

# 8. Document ingestion

We created a knowledge directory containing QA requirements.

The application reads documents and extracts their text.

Later, support was added for additional document formats.

------------------------------------------------------------------------

# 9. Chunking

Large documents should not always be passed to the LLM as one giant
block.

The document was split into smaller chunks.

Example:

``` text
Document
   ↓
Chunk 1
Chunk 2
Chunk 3
...
Chunk N
```

Each chunk becomes independently searchable.

------------------------------------------------------------------------

# 10. Embeddings

Text was converted into numerical vectors using:

``` text
nomic-embed-text
```

Example concept:

``` text
"Account locks after five failed attempts"
             ↓
      [0.12, -0.03, ...]
```

The vector represents semantic meaning.

This allows the system to search by meaning instead of only exact
keywords.

------------------------------------------------------------------------

# 11. Semantic search

A user's question is also converted into an embedding.

The system compares the question vector with document vectors.

Initially we implemented cosine similarity ourselves.

Concept:

``` text
Question embedding
       ↓
Compare against document embeddings
       ↓
Similarity scores
       ↓
Top relevant chunks
```

This proved that semantic retrieval was working.

------------------------------------------------------------------------

# 12. RAG generation

The retrieved chunks were placed into the LLM prompt as context.

Concept:

``` text
Retrieved documentation
        +
User question
        ↓
      Llama
        ↓
Grounded answer
```

The system prompt explicitly told the model not to invent information.

------------------------------------------------------------------------

# 13. ChromaDB

The first vector implementation stored embeddings in:

``` text
data/embeddings.json
```

This was useful for learning but not ideal as the long-term vector
layer.

We replaced it with ChromaDB.

``` text
Document
   ↓
Embedding
   ↓
ChromaDB
   ↓
Vector retrieval
```

This is a major architectural improvement.

------------------------------------------------------------------------

# 14. Requirement analysis

We then moved beyond a generic chatbot.

A dedicated requirement-analysis workflow was added.

The assistant can examine a requirement and identify:

-   What needs to be tested
-   Ambiguities
-   Missing details
-   Risks
-   Positive cases
-   Negative cases
-   Boundary cases

This makes the application specifically useful to QA engineers.

------------------------------------------------------------------------

# 15. Test-case generation

The project added structured AI test-case generation.

The generated output includes fields such as:

``` text
TC ID
Requirement ID
Requirement
Scenario
Test Type
Priority
Risk
Preconditions
Steps
Test Data
Expected Result
Traceability
```

The output is structured rather than being only free-form text.

------------------------------------------------------------------------

# 16. Test-case validation

AI output cannot automatically be trusted.

A validation layer was added.

It checks whether generated test cases contain the expected structure
and required information.

Concept:

``` text
LLM output
    ↓
Validator
    ↓
Valid / Invalid
```

This is important for AI QA because **AI-generated output itself must be
tested.**

------------------------------------------------------------------------

# 17. API testing

The project added an API testing workflow.

The assistant can receive an API description and generate/execute
API-oriented tests.

Concept:

``` text
API description
      ↓
AI
      ↓
API test generation
      ↓
Execution
      ↓
Assertions
      ↓
Result
```

------------------------------------------------------------------------

# 18. UI testing

A UI testing capability was added for browser-based testing.

The project can use AI to assist with creation/execution of UI test
workflows.

This connects LLM capabilities with traditional browser automation.

------------------------------------------------------------------------

# 19. Failure analysis

A failure-analysis workflow was added.

Input can include information such as:

``` text
Test type
Execution result
Failure information
```

The AI analyzes it and provides a useful interpretation.

Concept:

``` text
Failed test
    ↓
Failure analysis
    ↓
Possible cause
    ↓
Investigation guidance
```

------------------------------------------------------------------------

# 20. AI QA Agent

The project evolved from a chatbot into an AI QA agent.

Instead of only answering questions, the agent can coordinate QA
capabilities.

Concept:

``` text
User goal
   ↓
AI QA Agent
   ↓
Choose capability
   ├── Requirement Analysis
   ├── Test Generation
   ├── API Testing
   ├── UI Testing
   └── Failure Analysis
```

This is the difference between:

``` text
LLM chatbot
```

and:

``` text
AI system with tools/workflows
```

------------------------------------------------------------------------

# 21. Evaluation

AI output needs evaluation.

We added evaluation logic so that generated outputs can be checked
against expected criteria.

This introduces an important AI QA concept:

**Testing the AI system itself.**

Traditional QA asks:

> Does the application behave correctly?

AI QA also asks:

> Is the model output relevant, grounded, complete, and structurally
> valid?

------------------------------------------------------------------------

# 22. Configuration and security

Configuration was separated into dedicated modules.

Environment variables are used for configuration instead of hard-coding
secrets.

Security considerations were also added.

For a real production system, more work would still be required around:

-   Authentication
-   Authorization
-   Session ownership
-   Input validation
-   File upload security
-   Output sanitization
-   Rate limiting
-   Secrets
-   HTTPS
-   Audit logging

------------------------------------------------------------------------

# 23. Automated testing with Pytest

The project includes automated tests.

Final verification showed:

``` text
5 passed
```

This is important because the AI application itself is developed using
normal software engineering and QA practices.

------------------------------------------------------------------------

# 24. Docker

The application was containerized.

Build:

``` powershell
docker build -t qa-ai-assistant .
```

Run:

``` powershell
docker run -p 8000:8000 qa-ai-assistant
```

The final Docker image was created successfully and the container was
running on port 8000.

Concept:

``` text
Source code
    ↓
Dockerfile
    ↓
Docker image
    ↓
Docker container
    ↓
FastAPI application
```

------------------------------------------------------------------------

# 25. Git and GitHub

Git was initialized and the project was committed to GitHub.

The final repository is:

``` text
github.com/govindkumit/qa-ai-assistant
```

The repository contains the application source, tests, knowledge files,
Docker configuration, and CI workflow.

------------------------------------------------------------------------

# 26. GitHub Actions CI/CD

A GitHub Actions workflow was added.

When code is pushed:

``` text
git push
    ↓
GitHub
    ↓
GitHub Actions
    ↓
Install dependencies
    ↓
Run tests
    ↓
PASS / FAIL
```

The project successfully produced green workflow runs.

This proves the project has an automated validation pipeline rather than
relying only on manual testing.

------------------------------------------------------------------------

# 27. Final architecture

The final system can be understood as six major layers.

``` text
┌──────────────────────────────────────┐
│              Web UI                  │
│          HTML / CSS / JS             │
└──────────────────┬───────────────────┘
                   │
┌──────────────────▼───────────────────┐
│              FastAPI                 │
│              REST API                │
└──────────────────┬───────────────────┘
                   │
       ┌───────────┼────────────┐
       │           │            │
       ▼           ▼            ▼
 Requirement   Test Case     API/UI
 Analysis      Generation    Testing
       │           │            │
       └───────────┼────────────┘
                   │
┌──────────────────▼───────────────────┐
│             AI / RAG Layer           │
│                                      │
│ Ollama → Llama 3.2                   │
│ nomic-embed-text                     │
│ ChromaDB                             │
│ Prompting / Retrieval / Evaluation   │
└──────────────────┬───────────────────┘
                   │
       ┌───────────┼─────────────┐
       ▼           ▼             ▼
    SQLite      Knowledge      Testing
               Documents       / Pytest

Infrastructure:
Docker + GitHub + GitHub Actions
```

------------------------------------------------------------------------

# 28. What you learned by building it

The most important learning is not the individual files.

You learned how the pieces connect.

### AI

``` text
LLM
Prompt
Tokens
Embeddings
Vector Search
RAG
Agents
Evaluation
```

### QA

``` text
Requirement
Scenario
Test Case
API Test
UI Test
Failure Analysis
Validation
```

### Software Engineering

``` text
Python
FastAPI
REST
SQLite
Modular architecture
Configuration
```

### DevOps

``` text
Git
GitHub
Docker
CI/CD
```

------------------------------------------------------------------------

# 29. The most important interview concept

If asked:

**"What is the key architecture of your project?"**

Answer:

> "The application follows an AI-assisted QA architecture. FastAPI
> provides the service layer, SQLite handles conversation persistence,
> and the RAG layer ingests QA documentation, creates embeddings and
> stores them in ChromaDB. For each user request, relevant documentation
> is retrieved and passed as context to a local Llama 3.2 model through
> Ollama. On top of that foundation, I implemented QA-specific workflows
> such as requirement analysis, structured test-case generation and
> validation, API/UI testing, failure analysis, and an AI QA agent.
> Docker provides containerization and GitHub Actions provides automated
> CI validation."

------------------------------------------------------------------------

# 30. Final project state

The project is now a portfolio-ready **AI QA engineering
demonstration**.

``` text
AI + QA + Automation + RAG + Vector DB
                  +
API + UI Testing
                  +
Docker + GitHub + CI/CD
```

The implementation is complete enough for portfolio and interview
demonstration.

The next focus should be:

1.  Understand every major component.
2.  Understand why each technology was chosen.
3.  Practice the architecture explanation.
4.  Practice the project walkthrough.
5.  Prepare interview questions around AI QA.
