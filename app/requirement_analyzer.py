import json

import ollama

from app.search import search
from app.rag import build_context


LLM_MODEL = "llama3.2"


def analyze_requirement(
    requirement,
    top_k=5
):
    """
    Analyze a software requirement from
    a QA Architect perspective.
    """

    # -----------------------------------------
    # 1. Retrieve relevant documentation
    # -----------------------------------------

    results = search(
        requirement,
        top_k=top_k
    )

    # -----------------------------------------
    # 2. Build documentation context
    # -----------------------------------------

    context = build_context(
        results
    )

    # -----------------------------------------
    # 3. Build analysis prompt
    # -----------------------------------------

    prompt = f"""
You are a Senior QA Architect and
AI QA Requirements Analyst.

Your task is to analyze the user's software
requirement before test cases are created.

Use the provided documentation as the
primary source of truth.

==================================================
IMPORTANT RULES
==================================================

1. Do not invent application behavior.

2. Clearly distinguish between:

   - Explicitly stated information
   - Missing information
   - Ambiguities
   - QA recommendations

3. Do not assume unspecified business rules.

4. Identify unclear or incomplete requirements.

5. Identify missing acceptance criteria.

6. Identify testable scenarios that are directly
   supported by the requirement or documentation.

7. Identify positive scenarios.

8. Identify negative scenarios.

9. Identify boundary conditions when applicable.

10. Identify edge cases when applicable.

11. Identify potential QA risks.

12. Identify questions that should be asked
    to the Product Owner / Business Analyst.

13. Give the requirement a quality rating:

    High
    Medium
    Low

14. Give separate scores from 0 to 100 for:

    clarity
    completeness
    testability

15. Return ONLY valid JSON.

==================================================
REQUIRED JSON STRUCTURE
==================================================

{{
    "requirement_analysis": {{
        "quality": "High",
        "clarity_score": 80,
        "completeness_score": 70,
        "testability_score": 75,

        "requirement_summary":
            "Short summary of the requirement.",

        "explicit_requirements": [
            "Explicit requirement 1"
        ],

        "ambiguities": [
            "Ambiguous point 1"
        ],

        "missing_information": [
            "Missing information 1"
        ],

        "missing_acceptance_criteria": [
            "Acceptance criterion 1"
        ],

        "positive_scenarios": [
            "Positive scenario 1"
        ],

        "negative_scenarios": [
            "Negative scenario 1"
        ],

        "boundary_conditions": [
            "Boundary condition 1"
        ],

        "edge_cases": [
            "Edge case 1"
        ],

        "qa_risks": [
            "Potential QA risk 1"
        ],

        "questions_for_product_owner": [
            "Question 1"
        ],

        "recommendations": [
            "Recommendation 1"
        ]
    }}
}}

==================================================
DOCUMENTATION CONTEXT
==================================================

{context}

==================================================
USER REQUIREMENT
==================================================

{requirement}
"""

    # -----------------------------------------
    # 4. Ask Llama
    # -----------------------------------------

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Senior QA Architect "
                    "specialized in requirement analysis."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    content = response[
        "message"
    ][
        "content"
    ]

    # -----------------------------------------
    # 5. Parse JSON
    # -----------------------------------------

    try:

        result = json.loads(
            content
        )

    except json.JSONDecodeError:

        return {
            "requirement_analysis": {},
            "error": (
                "The AI returned invalid JSON."
            ),
            "sources": results
        }

    # -----------------------------------------
    # 6. Return analysis + sources
    # -----------------------------------------

    return {
        "requirement_analysis":
            result.get(
                "requirement_analysis",
                {}
            ),

        "sources": results
    }


if __name__ == "__main__":

    requirement = """
Users should be able to register using
a username and email address.
"""

    result = analyze_requirement(
        requirement
    )

    print("\n")
    print("=" * 70)
    print("REQUIREMENT ANALYSIS")
    print("=" * 70)

    print(
        json.dumps(
            result["requirement_analysis"],
            indent=2
        )
    )

    print("\n")
    print("=" * 70)
    print("SOURCES")
    print("=" * 70)

    for source in result["sources"]:

        print(
            f"- {source['source']} "
            f"(chunk {source['chunk_id']}, "
            f"distance "
            f"{source['distance']:.4f})"
        )