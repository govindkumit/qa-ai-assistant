import json

from app.failure_analyzer import (
    analyze_test_failure
)


def analyze_failed_tests(
    test_type,
    execution_result
):

    results = execution_result.get(
        "results",
        []
    )


    failed_tests = [
        result
        for result in results
        if not result.get("passed")
    ]


    analyses = []


    for failed_test in failed_tests:

        analysis = analyze_test_failure(
            test_type,
            failed_test
        )


        analyses.append(
            {
                "test_case":
                    failed_test,

                "analysis":
                    analysis
            }
        )


    return {
        "test_type":
            test_type,

        "total_failures":
            len(failed_tests),

        "defects":
            analyses
    }


if __name__ == "__main__":

    execution_result = {
        "total": 1,

        "passed": 0,

        "failed": 1,

        "results": [
            {
                "test_case_id":
                    "UI-TC-001",

                "name":
                    "Verify login button",

                "passed":
                    False,

                "url":
                    "https://example.com",

                "error":
                    "Locator '#login' not found",

                "screenshot":
                    "data/screenshots/UI-TC-001.png"
            }
        ]
    }


    result = analyze_failed_tests(
        "UI",
        execution_result
    )


    print("\n")
    print("=" * 70)
    print("FAILURE + DEFECT ANALYSIS")
    print("=" * 70)


    print(
        json.dumps(
            result,
            indent=2
        )
    )