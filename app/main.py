from contextlib import asynccontextmanager
from pathlib import Path
import shutil
import subprocess

import ollama

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from app.db import (
    init_db,
    create_session,
    add_message,
    get_messages
)

from app.prompts import SYSTEM_PROMPT

from app.search import search

from app.rag import build_context

from app.test_generator import (
    generate_test_cases
)

from app.requirement_analyzer import (
    analyze_requirement
)

from app.api_testing import (
    generate_and_execute_api_tests
)

from app.ui_testing import (
    generate_and_execute_ui_tests
)

from app.failure_defect_analysis import (
    analyze_failed_tests
)

from app.qa_agent import (
    run_agent
)


LLM_MODEL = "llama3.2"

KNOWLEDGE_DIR = Path("knowledge")


# ============================================================
# APPLICATION STARTUP
# ============================================================

@asynccontextmanager
async def lifespan(app):

    init_db()

    KNOWLEDGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    yield


app = FastAPI(
    lifespan=lifespan
)


app.mount(
    "/static",
    StaticFiles(
        directory="static"
    ),
    name="static"
)


# ============================================================
# REQUEST MODELS
# ============================================================

class ChatRequest(BaseModel):

    session_id: str
    message: str


class TestCaseRequest(BaseModel):

    requirement: str


class RequirementAnalysisRequest(BaseModel):

    requirement: str


class APITestRequest(BaseModel):

    api_description: str


class UITestRequest(BaseModel):

    requirement: str


class FailureAnalysisRequest(BaseModel):

    test_type: str

    execution_result: dict


class AgentRequest(BaseModel):

    message: str

    test_type: str | None = None

    execution_result: dict | None = None


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return FileResponse(
        "static/index.html"
    )


# ============================================================
# DOCUMENT UPLOAD
# ============================================================

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".txt",
        ".pdf",
        ".docx",
        ".xlsx"
    }


    extension = Path(
        file.filename
    ).suffix.lower()


    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Use TXT, PDF, DOCX or XLSX."
            )
        )


    destination = (
        KNOWLEDGE_DIR /
        Path(file.filename).name
    )


    with destination.open(
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    try:

        subprocess.run(
            [
                "python",
                "-m",
                "app.build_embeddings"
            ],
            check=True
        )


        subprocess.run(
            [
                "python",
                "-m",
                "app.index_vectors"
            ],
            check=True
        )


    except subprocess.CalledProcessError:

        raise HTTPException(
            status_code=500,
            detail=(
                "Document uploaded, "
                "but indexing failed."
            )
        )


    return {
        "message":
            f"{file.filename} uploaded "
            "and indexed successfully."
    }


# ============================================================
# CHAT / RAG
# ============================================================

@app.post("/chat")
def chat(
    request: ChatRequest
):

    session_id = request.session_id


    create_session(
        session_id
    )


    history = get_messages(
        session_id
    )


    results = search(
        request.message,
        top_k=5
    )


    context = build_context(
        results
    )


    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


    messages.extend(
        history
    )


    rag_prompt = f"""
Use the provided documentation context
to answer the user's question.

IMPORTANT RULES:

1. Use the documentation when relevant.

2. Do not invent requirements or facts.

3. If the documentation does not contain
   enough information, clearly say so.

4. Prefer documentation over general knowledge.

5. Keep the answer clear and concise.

DOCUMENTATION CONTEXT:

{context}

USER QUESTION:

{request.message}
"""


    messages.append(
        {
            "role": "user",
            "content": rag_prompt
        }
    )


    add_message(
        session_id,
        "user",
        request.message
    )


    response = ollama.chat(
        model=LLM_MODEL,
        messages=messages
    )


    assistant_message = (
        response["message"]["content"]
    )


    add_message(
        session_id,
        "assistant",
        assistant_message
    )


    sources = []


    for result in results:

        sources.append(
            {
                "source":
                    result["source"],

                "chunk_id":
                    result["chunk_id"],

                "distance":
                    round(
                        result["distance"],
                        4
                    )
            }
        )


    return {
        "response":
            assistant_message,

        "sources":
            sources
    }


# ============================================================
# TEST CASE GENERATION
# ============================================================

@app.post(
    "/generate-test-cases"
)
def generate_test_cases_endpoint(
    request: TestCaseRequest
):

    if not request.requirement.strip():

        raise HTTPException(
            status_code=400,
            detail=
                "Requirement cannot be empty."
        )


    return generate_test_cases(
        request.requirement
    )


# ============================================================
# REQUIREMENT ANALYSIS
# ============================================================

@app.post(
    "/analyze-requirement"
)
def analyze_requirement_endpoint(
    request:
        RequirementAnalysisRequest
):

    if not request.requirement.strip():

        raise HTTPException(
            status_code=400,
            detail=
                "Requirement cannot be empty."
        )


    return analyze_requirement(
        request.requirement
    )


# ============================================================
# API TESTING
# ============================================================

@app.post(
    "/api-test"
)
def api_test_endpoint(
    request: APITestRequest
):

    if not request.api_description.strip():

        raise HTTPException(
            status_code=400,
            detail=
                "API description cannot be empty."
        )


    return generate_and_execute_api_tests(
        request.api_description
    )


# ============================================================
# UI TESTING
# ============================================================

@app.post(
    "/ui-test"
)
def ui_test_endpoint(
    request: UITestRequest
):

    if not request.requirement.strip():

        raise HTTPException(
            status_code=400,
            detail=
                "UI requirement cannot be empty."
        )


    return generate_and_execute_ui_tests(
        request.requirement
    )


# ============================================================
# FAILURE + DEFECT ANALYSIS
# ============================================================

@app.post(
    "/analyze-failure"
)
def analyze_failure_endpoint(
    request:
        FailureAnalysisRequest
):

    if not request.test_type.strip():

        raise HTTPException(
            status_code=400,
            detail=
                "test_type cannot be empty."
        )


    return analyze_failed_tests(
        request.test_type,
        request.execution_result
    )


# ============================================================
# AI QA AGENT
# ============================================================

@app.post(
    "/agent"
)
def agent_endpoint(
    request: AgentRequest
):

    if not request.message.strip():

        raise HTTPException(
            status_code=400,
            detail=
                "Agent message cannot be empty."
        )


    return run_agent(
        message=request.message,

        execution_result=
            request.execution_result,

        test_type=
            request.test_type
    )


# ============================================================
# HISTORY
# ============================================================

@app.get(
    "/history/{session_id}"
)
def get_history(
    session_id: str
):

    messages = get_messages(
        session_id
    )


    return {
        "messages": messages
    }