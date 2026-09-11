import json

from app.search import search
from app.rag import build_context

from app.test_generator import (
    generate_test_cases
)

from app.requirement_analyzer import (
    analyze_requirement
)

from app.api_testing import (
    generate_and_execute_api_tests
)

from app.ui_testing import (
    generate_and_execute_ui_tests
)

from app.failure_defect_analysis import (
    analyze_failed_tests
)


# ============================================================
# TOOL DEFINITIONS
# ============================================================

def knowledge_search_tool(
    question
):

    results = search(
        question,
        top_k=5
    )

    context = build_context(
        results
    )

    return {
        "tool":
            "knowledge_search",

        "question":
            question,

        "context":
            context,

        "sources":
            [
                {
                    "source":
                        result["source"],

                    "chunk_id":
                        result["chunk_id"],

                    "distance":
                        result["distance"]
                }

                for result in results
            ]
    }


def requirement_analysis_tool(
    requirement
):

    return analyze_requirement(
        requirement
    )


def test_generation_tool(
    requirement
):

    return generate_test_cases(
        requirement
    )


def api_testing_tool(
    api_description
):

    return generate_and_execute_api_tests(
        api_description
    )


def ui_testing_tool(
    requirement
):

    return generate_and_execute_ui_tests(
        requirement
    )


def failure_analysis_tool(
    test_type,
    execution_result
):

    return analyze_failed_tests(
        test_type,
        execution_result
    )


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(
    message
):

    text = message.lower()


    # Failure analysis
    if any(
        keyword in text
        for keyword in [
            "failure",
            "failed test",
            "test failed",
            "root cause",
            "defect",
            "bug analysis"
        ]
    ):

        return "failure_analysis"


    # API testing
    if any(
        keyword in text
        for keyword in [
            "api test",
            "api testing",
            "rest api",
            "endpoint",
            "api"
        ]
    ):

        return "api_testing"


    # UI / Playwright testing
    if any(
        keyword in text
        for keyword in [
            "playwright",
            "ui test",
            "ui testing",
            "browser test",
            "web test",
            "frontend test"
        ]
    ):

        return "ui_testing"


    # Test generation
    if any(
        keyword in text
        for keyword in [
            "generate test",
            "test cases",
            "test case",
            "test scenarios",
            "test scenario"
        ]
    ):

        return "test_generation"


    # Requirement analysis
    if any(
        keyword in text
        for keyword in [
            "analyze requirement",
            "analyse requirement",
            "requirement analysis",
            "ambiguity",
            "missing requirement"
        ]
    ):

        return "requirement_analysis"


    # Default = knowledge / RAG
    return "knowledge_search"


# ============================================================
# AGENT EXECUTION
# ============================================================

def run_agent(
    message,
    execution_result=None,
    test_type=None
):

    intent = detect_intent(
        message
    )


    # --------------------------------------------------------
    # Knowledge Search
    # --------------------------------------------------------

    if intent == "knowledge_search":

        result = knowledge_search_tool(
            message
        )


    # --------------------------------------------------------
    # Requirement Analysis
    # --------------------------------------------------------

    elif intent == "requirement_analysis":

        result = requirement_analysis_tool(
            message
        )


    # --------------------------------------------------------
    # Test Generation
    # --------------------------------------------------------

    elif intent == "test_generation":

        result = test_generation_tool(
            message
        )


    # --------------------------------------------------------
    # API Testing
    # --------------------------------------------------------

    elif intent == "api_testing":

        result = api_testing_tool(
            message
        )


    # --------------------------------------------------------
    # UI Testing
    # --------------------------------------------------------

    elif intent == "ui_testing":

        result = ui_testing_tool(
            message
        )


    # --------------------------------------------------------
    # Failure Analysis
    # --------------------------------------------------------

    elif intent == "failure_analysis":

        if execution_result is None:

            return {
                "agent":
                    "QA Agent",

                "intent":
                    intent,

                "error":
                    (
                        "Execution result is required "
                        "for failure analysis."
                    )
            }


        result = failure_analysis_tool(
            test_type or "Unknown",
            execution_result
        )


    else:

        result = {
            "error":
                "Unknown agent intent."
        }


    return {
        "agent":
            "QA Agent",

        "intent":
            intent,

        "result":
            result
    }


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    examples = [

        "What are the requirements for registration?",

        "Generate test cases for username registration.",

        "Analyze requirement: username must be unique.",

        "Run API tests for GET https://example.com",

        "Create Playwright UI tests for the login page."
    ]


    print("\n")
    print("=" * 70)
    print("AI QA AGENT")
    print("=" * 70)


    for message in examples:

        intent = detect_intent(
            message
        )

        print(
            f"\nMessage: {message}"
        )

        print(
            f"Selected tool: {intent}"
        )