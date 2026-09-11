import json

import ollama


LLM_MODEL = "llama3.2"


def generate_ui_test(
    requirement
):

    prompt = f"""
You are a Senior QA Automation Architect
specialized in Playwright.

Create a UI automation test plan for the
requirement below.

REQUIREMENT:

{requirement}

IMPORTANT RULES:

1. Return ONLY valid JSON.

2. Use Playwright with Python.

3. Generate a maximum of 5 test cases.

4. Include positive and negative scenarios
   when applicable.

5. Every test must contain:

   test_case_id
   name
   test_type
   url
   actions
   expected_result

6. Each action must contain:

   action
   locator
   value

7. Supported actions are:

   navigate
   click
   fill
   press

8. Use realistic CSS selectors.

9. Do not invent unnecessary application
   behavior.

10. Keep the tests executable.

Use this exact structure:

{{
    "ui_tests": [
        {{
            "test_case_id": "UI-TC-001",
            "name": "Successful login",
            "test_type": "Positive",
            "url": "https://example.com",
            "actions": [
                {{
                    "action": "navigate",
                    "locator": "",
                    "value": "https://example.com"
                }},
                {{
                    "action": "fill",
                    "locator": "#username",
                    "value": "testuser"
                }},
                {{
                    "action": "fill",
                    "locator": "#password",
                    "value": "Password123"
                }},
                {{
                    "action": "click",
                    "locator": "#login",
                    "value": ""
                }}
            ],
            "expected_result":
                "User is successfully logged in."
        }}
    ]
}}

REQUIREMENT:

{requirement}
"""


    response = ollama.chat(
        model=LLM_MODEL,

        messages=[
            {
                "role": "system",
                "content":
                    "You are a Senior QA "
                    "Automation Architect."
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

        result = json.loads(
            content
        )

    except json.JSONDecodeError:

        return {
            "ui_tests": [],
            "error":
                "AI returned invalid JSON."
        }


    tests = result.get(
        "ui_tests",
        []
    )


    if not isinstance(
        tests,
        list
    ):

        tests = []


    return {
        "ui_tests":
            tests[:5]
    }


if __name__ == "__main__":

    requirement = """
Open https://example.com and verify
that the page contains the heading
"Example Domain".
"""


    result = generate_ui_test(
        requirement
    )


    print("\n")
    print("=" * 70)
    print("AI UI TESTS")
    print("=" * 70)


    print(
        json.dumps(
            result,
            indent=2
        )
    )