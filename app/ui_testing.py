import json

from app.ui_test_generator import (
    generate_ui_test
)

from app.ui_test_runner import (
    execute_ui_tests
)


def generate_and_execute_ui_tests(
    requirement,
    headless=True
):

    generated = generate_ui_test(
        requirement
    )


    test_cases = generated.get(
        "ui_tests",
        []
    )


    if not test_cases:

        return {
            "ui_tests": [],

            "execution": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "results": []
            },

            "error":
                generated.get(
                    "error",
                    "No UI tests generated."
                )
        }


    execution = execute_ui_tests(
        test_cases,
        headless=headless
    )


    return {
        "ui_tests":
            test_cases,

        "execution":
            execution
    }


if __name__ == "__main__":

    requirement = """
Open https://example.com and verify
that the page contains the heading
"Example Domain".
"""


    result = generate_and_execute_ui_tests(
        requirement
    )


    print("\n")
    print("=" * 70)
    print("AI GENERATED UI TESTS")
    print("=" * 70)


    print(
        json.dumps(
            result["ui_tests"],
            indent=2
        )
    )


    print("\n")
    print("=" * 70)
    print("PLAYWRIGHT EXECUTION")
    print("=" * 70)


    print(
        json.dumps(
            result["execution"],
            indent=2
        )
    )