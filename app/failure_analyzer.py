import json

import ollama


LLM_MODEL = "llama3.2"


def analyze_failure(
    failure_data
):
    """
    Analyze a failed API or UI test and
    generate structured root-cause and
    defect information.
    """

    failure_json = json.dumps(
        failure_data,
        indent=2
    )


    prompt = f"""
You are a Senior QA Architect and
AI Defect Analysis Expert.

Analyze the following automated test
failure.

FAILURE DATA:

{failure_json}

IMPORTANT RULES:

1. Return ONLY valid JSON.

2. Do not invent facts that are not
   supported by the failure information.

3. Clearly distinguish between:

   - confirmed evidence
   - likely root cause
   - recommendation

4. If the root cause cannot be determined
   with confidence, say:

   "Root cause requires further investigation."

5. Determine:

   - failure_summary
   - root_cause
   - root_cause_category
   - severity
   - priority
   - bug_title
   - steps_to_reproduce
   - expected_result
   - actual_result
   - recommendation

6. Severity must be one of:

   Critical
   High
   Medium
   Low

7. Priority must be one of:

   P0
   P1
   P2
   P3

8. root_cause_category must be one of:

   Application Defect
   Test Automation Defect
   Environment Issue
   Network Issue
   Data Issue
   Unknown

Use exactly this structure:

{{
    "failure_summary":
        "Short description of failure.",

    "root_cause":
        "Most likely root cause.",

    "root_cause_category":
        "Application Defect",

    "severity":
        "High",

    "priority":
        "P1",

    "bug_title":
        "Clear concise defect title.",

    "steps_to_reproduce": [
        "Step 1",
        "Step 2",
        "Step 3"
    ],

    "expected_result":
        "Expected behavior.",

    "actual_result":
        "Actual behavior.",

    "recommendation":
        "Recommended next action."
}}

FAILURE DATA:

{failure_json}
"""


    response = ollama.chat(
        model=LLM_MODEL,

        messages=[
            {
                "role": "system",

                "content":
                    "You are an expert QA "
                    "failure and defect analyst."
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
            "failure_summary":
                "Unable to parse AI analysis.",

            "root_cause":
                "Root cause requires further investigation.",

            "root_cause_category":
                "Unknown",

            "severity":
                "Medium",

            "priority":
                "P2",

            "bug_title":
                "Automated test failure",

            "steps_to_reproduce": [],

            "expected_result":
                "",

            "actual_result":
                "",

            "recommendation":
                "Review the automation failure manually."
        }


    return result


def analyze_test_failure(
    test_type,
    test_result
):

    failure_data = {
        "test_type":
            test_type,

        "test_result":
            test_result
    }


    return analyze_failure(
        failure_data
    )


if __name__ == "__main__":

    failure = {
        "test_case_id":
            "UI-TC-001",

        "name":
            "Verify login button",

        "method":
            "UI",

        "url":
            "https://example.com",

        "passed":
            False,

        "error":
            "Locator '#login' not found",

        "screenshot":
            "data/screenshots/UI-TC-001.png"
    }


    result = analyze_test_failure(
        "UI",
        failure
    )


    print("\n")
    print("=" * 70)
    print("AI FAILURE ANALYSIS")
    print("=" * 70)


    print(
        json.dumps(
            result,
            indent=2
        )
    )