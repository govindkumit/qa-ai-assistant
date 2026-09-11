import ollama

from app.search import search
from app.prompts import SYSTEM_PROMPT

LLM_MODEL = "llama3.2"


def build_context(results):
    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['source']}\n"
            f"Chunk: {result['chunk_id']}\n"
            f"Content:\n{result['text']}"
        )

    return "\n\n".join(context_parts)


def generate_answer(question):
    results = search(question, top_k=3)

    context = build_context(results)

    prompt = f"""
Use the following context to answer the user's question.

IMPORTANT RULES:

- Answer using the provided context.
- Do not invent information.
- If the answer cannot be found in the context,
  say that the information is not available
  in the provided documentation.
- Prefer information from the context over
  your general knowledge.

CONTEXT:

{context}

USER QUESTION:

{question}
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response["message"]["content"],
        "sources": results
    }


if __name__ == "__main__":

    question = (
        "How many wrong passwords "
        "can I enter before my account "
        "is locked?"
    )

    result = generate_answer(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(
            f"- {source['source']} "
            f"(chunk {source['chunk_id']}, "
            f"distance {source['distance']:.4f})"
        )