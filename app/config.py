import os

from dotenv import load_dotenv


load_dotenv()


LLM_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)


EMBEDDING_MODEL = os.getenv(
    "OLLAMA_EMBEDDING_MODEL",
    "nomic-embed-text"
)


API_KEY = os.getenv(
    "API_KEY",
    ""
)