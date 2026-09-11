import json

import ollama


LLM_MODEL = "llama3.2"


def generate_api_tests(
    api_description
):
    """
    Generate structured API test cases
    from an API description.
    """

    prompt = f"""
You are an expert API Test Architect.

Generate comprehensive API test cases for
the API described below.

API DESCRIPTION:

{api_description}

IMPORTANT RULES:

1. Return ONLY valid JSON.

2. Generate positive and negative tests.

3. Consider:

   - HTTP method
   - URL
   - Status codes
   - Request body
   - Query parameters
   - Headers
   - Authentication when applicable
   - Required fields
   - Invalid fields
   - Boundary values
   - Response validation

4. Do not invent authentication requirements
   if they are not provided.

5. Every test must contain enough information
   for Python requests to execute it.

Use exactly this JSON structure:

{{
    "api_tests": [
        {{
            "test_case_id": "API-TC-001",
            "name": "Valid API request",
            "method": "GET",
            "url": "https://example.com/api/users/1",
            "headers": {{}},
            "query_params": {{}},
            "body": null,
            "expected_status": 200,
            "test_type": "Positive",
            "expected_response_contains": []
        }}
    ]
}}

API DESCRIPTION:

{api_description}
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert API "
                    "test architect."
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

    try:

        result = json.loads(
            content
        )

    except json.JSONDecodeError:

        return {
            "api_tests": [],
            "error": "AI returned invalid JSON."
        }

    return result


if __name__ == "__main__":

    api_description = """
GET https://jsonplaceholder.typicode.com/users/1

This API returns information about a user.
"""

    result = generate_api_tests(
        api_description
    )

    print("\n")
    print("=" * 70)
    print("AI API TEST CASES")
    print("=" * 70)

    print(
        json.dumps(
            result,
            indent=2
        )
    )