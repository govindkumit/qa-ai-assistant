import json

from app.api_test_generator import (
    generate_api_tests
)

from app.api_test_runner import (
    execute_api_tests
)


def generate_and_execute_api_tests(
    api_description
):

    # -----------------------------------------
    # Generate tests using AI
    # -----------------------------------------

    generated = generate_api_tests(
        api_description
    )


    test_cases = generated.get(
        "api_tests",
        []
    )


    if not test_cases:

        return {
            "api_tests": [],
            "execution": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "results": []
            },
            "error":
                generated.get(
                    "error",
                    "No API tests generated."
                )
        }


    # -----------------------------------------
    # Execute generated tests
    # -----------------------------------------

    execution = execute_api_tests(
        test_cases
    )


    return {
        "api_tests": test_cases,
        "execution": execution
    }


if __name__ == "__main__":

    api_description = """
GET https://jsonplaceholder.typicode.com/users/1

The endpoint returns a user object.
"""

    result = (
        generate_and_execute_api_tests(
            api_description
        )
    )


    print("\n")
    print("=" * 70)
    print("GENERATED API TESTS")
    print("=" * 70)

    print(
        json.dumps(
            result["api_tests"],
            indent=2
        )
    )


    print("\n")
    print("=" * 70)
    print("EXECUTION RESULT")
    print("=" * 70)

    print(
        json.dumps(
            result["execution"],
            indent=2
        )
    )