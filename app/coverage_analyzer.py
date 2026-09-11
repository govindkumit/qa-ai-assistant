from collections import Counter


SUPPORTED_TEST_TYPES = {
    "Positive",
    "Negative",
    "Boundary",
    "Edge"
}


def analyze_test_coverage(test_cases):
    """
    Analyze generated test cases and calculate
    coverage statistics.
    """

    total_test_cases = len(
        test_cases
    )

    # -----------------------------------------
    # Count test types
    # -----------------------------------------

    type_counts = Counter()

    for test_case in test_cases:

        test_type = test_case.get(
            "test_type",
            "Unknown"
        )

        type_counts[test_type] += 1


    # -----------------------------------------
    # Calculate test-type coverage
    # -----------------------------------------

    positive_count = type_counts.get(
        "Positive",
        0
    )

    negative_count = type_counts.get(
        "Negative",
        0
    )

    boundary_count = type_counts.get(
        "Boundary",
        0
    )

    edge_count = type_counts.get(
        "Edge",
        0
    )


    # -----------------------------------------
    # Requirements covered
    # -----------------------------------------

    requirement_ids = set()

    for test_case in test_cases:

        requirement_id = test_case.get(
            "requirement_id"
        )

        if requirement_id:

            requirement_ids.add(
                requirement_id
            )


    requirements_covered = len(
        requirement_ids
    )


    # -----------------------------------------
    # Determine coverage categories
    # -----------------------------------------

    coverage_categories = []

    if positive_count > 0:

        coverage_categories.append(
            "Positive"
        )

    if negative_count > 0:

        coverage_categories.append(
            "Negative"
        )

    if boundary_count > 0:

        coverage_categories.append(
            "Boundary"
        )

    if edge_count > 0:

        coverage_categories.append(
            "Edge"
        )


    # -----------------------------------------
    # Coverage score
    # -----------------------------------------

    possible_categories = 4

    category_score = (
        len(coverage_categories)
        / possible_categories
    ) * 100


    # -----------------------------------------
    # Test-case quality
    # -----------------------------------------

    valid_test_cases = 0

    for test_case in test_cases:

        required_fields = [
            "test_case_id",
            "requirement_id",
            "scenario",
            "test_type",
            "expected_result",
            "traceability"
        ]

        if all(
            field in test_case
            for field in required_fields
        ):

            valid_test_cases += 1


    if total_test_cases > 0:

        quality_score = (
            valid_test_cases
            / total_test_cases
        ) * 100

    else:

        quality_score = 0


    # -----------------------------------------
    # Overall score
    # -----------------------------------------

    overall_score = (
        category_score * 0.5
        +
        quality_score * 0.5
    )


    return {
        "total_test_cases": total_test_cases,

        "requirements_covered":
            requirements_covered,

        "test_type_counts": {
            "Positive": positive_count,
            "Negative": negative_count,
            "Boundary": boundary_count,
            "Edge": edge_count
        },

        "coverage_categories":
            coverage_categories,

        "category_coverage_percentage":
            round(
                category_score,
                2
            ),

        "quality_percentage":
            round(
                quality_score,
                2
            ),

        "overall_coverage_percentage":
            round(
                overall_score,
                2
            )
    }


def find_coverage_gaps(
    test_cases
):
    """
    Identify missing test categories.
    """

    existing_types = set()

    for test_case in test_cases:

        test_type = test_case.get(
            "test_type"
        )

        if test_type:

            existing_types.add(
                test_type
            )


    missing_types = (
        SUPPORTED_TEST_TYPES
        - existing_types
    )


    return sorted(
        missing_types
    )


if __name__ == "__main__":

    sample_test_cases = [

        {
            "test_case_id": "TC-001",
            "requirement_id": "REQ-001",
            "scenario": "Valid registration",
            "test_type": "Positive",
            "expected_result":
                "Registration succeeds.",
            "traceability": "REQ-001"
        },

        {
            "test_case_id": "TC-002",
            "requirement_id": "REQ-001",
            "scenario": "Duplicate username",
            "test_type": "Negative",
            "expected_result":
                "Registration is rejected.",
            "traceability": "REQ-001"
        },

        {
            "test_case_id": "TC-003",
            "requirement_id": "REQ-002",
            "scenario": "Boundary username",
            "test_type": "Boundary",
            "expected_result":
                "Validation behaves correctly.",
            "traceability": "REQ-002"
        }
    ]


    coverage = analyze_test_coverage(
        sample_test_cases
    )

    gaps = find_coverage_gaps(
        sample_test_cases
    )


    print("\nCOVERAGE ANALYSIS")
    print("=" * 60)

    print(
        coverage
    )

    print("\nCOVERAGE GAPS")
    print("=" * 60)

    print(
        gaps
    )