import json

import ollama

from app.vector_search import search_vectors

from app.evaluator import (
    validate_test_case,
    validate_test_cases,
    analyze_coverage,
    find_coverage_gaps,
    evaluate_test_generation
)


LLM_MODEL = "llama3.2"


def build_context(
    results
):

    if not results:

        return (
            "No relevant documentation found."
        )


    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]


    context_parts = []


    for index, document in enumerate(
        documents
    ):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )


        distance = (
            distances[index]
            if index < len(distances)
            else 0
        )


        context_parts.append(
            f"Source: "
            f"{metadata.get('source', 'unknown')}\n"

            f"Document: "
            f"{metadata.get('document_name', 'unknown')}\n"

            f"Type: "
            f"{metadata.get('document_type', 'unknown')}\n"

            f"Category: "
            f"{metadata.get('category', 'unknown')}\n"

            f"Chunk: "
            f"{metadata.get('chunk_id', 'unknown')}\n"

            f"Distance: "
            f"{distance:.4f}\n"

            f"Content:\n"
            f"{document}"
        )


    return "\n\n".join(
        context_parts
    )


def generate_test_cases(
    requirement,
    top_k=5
):

    results = search_vectors(
        requirement,
        top_k=top_k
    )


    context = build_context(
        results
    )


    prompt = f"""
You are a Senior QA Architect.

Generate comprehensive software test cases
for the requirement below.

Use the documentation context as the
primary source of truth.

IMPORTANT RULES:

1. Return ONLY valid JSON.

2. Generate between 4 and 10 test cases.

3. Cover Positive, Negative, Boundary and
   Edge cases whenever applicable.

4. Do not invent business requirements.

5. Every test case must contain all
   required fields.

6. test_steps must be an array.

7. preconditions must be an array.

8. expected_result must be specific
   and testable.

9. traceability must reference the
   requirement_id.

10. Return ONLY JSON.

JSON FORMAT:

{{
    "test_cases": [
        {{
            "test_case_id": "TC-001",
            "requirement_id": "REQ-001",
            "requirement": "Requirement text",
            "scenario": "Test scenario",
            "test_type": "Positive",
            "priority": "High",
            "risk": "Medium",
            "preconditions": [],
            "test_steps": [],
            "test_data": "Test data",
            "expected_result": "Expected result",
            "traceability": "REQ-001"
        }}
    ]
}}

DOCUMENTATION:

{context}

REQUIREMENT:

{requirement}
"""


    response = ollama.chat(
        model=LLM_MODEL,

        messages=[
            {
                "role": "system",
                "content":
                    "You are an expert QA Architect."
            },

            {
                "role": "user",
                "content":
                    prompt
            }
        ],

        format="json"
    )


    content = response[
        "message"
    ][
        "content"
    ]


    try:

        generated = json.loads(
            content
        )

    except json.JSONDecodeError:

        return {
            "test_cases": [],

            "validation": {
                "valid": False,
                "errors": [
                    "AI returned invalid JSON."
                ]
            },

            "coverage": {},

            "coverage_gaps": [],

            "evaluation": {
                "overall_score": 0,
                "rating": "Poor"
            },

            "sources":
                convert_sources(
                    results
                )
        }


    test_cases = generated.get(
        "test_cases",
        []
    )


    if not isinstance(
        test_cases,
        list
    ):

        test_cases = []


    test_cases = test_cases[:10]


    validation = validate_test_cases(
        test_cases
    )


    coverage = analyze_coverage(
        test_cases
    )


    coverage_gaps = find_coverage_gaps(
        test_cases
    )


    evaluation = evaluate_test_generation(
        requirement,
        generated
    )


    return {
        "test_cases":
            test_cases,

        "validation":
            validation,

        "coverage":
            coverage,

        "coverage_gaps":
            coverage_gaps,

        "evaluation":
            evaluation,

        "sources":
            convert_sources(
                results
            )
    }


def convert_sources(
    results
):

    sources = []


    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]


    for index in range(
        len(documents)
    ):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )


        distance = (
            distances[index]
            if index < len(distances)
            else 0
        )


        sources.append(
            {
                "source":
                    metadata.get(
                        "source",
                        "unknown"
                    ),

                "chunk_id":
                    metadata.get(
                        "chunk_id",
                        0
                    ),

                "distance":
                    distance
            }
        )


    return sources


if __name__ == "__main__":

    requirement = """
Users must provide a unique username
during registration.
"""


    result = generate_test_cases(
        requirement
    )


    print("\n")
    print("=" * 70)
    print("AI TEST GENERATION + EVALUATION")
    print("=" * 70)


    print(
        json.dumps(
            result,
            indent=2
        )
    )