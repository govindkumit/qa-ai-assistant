import re


# ============================================================
# REQUIRED TEST CASE FIELDS
# ============================================================

REQUIRED_TEST_FIELDS = [
    "test_case_id",
    "requirement_id",
    "requirement",
    "scenario",
    "test_type",
    "priority",
    "risk",
    "preconditions",
    "test_steps",
    "test_data",
    "expected_result",
    "traceability"
]


VALID_TEST_TYPES = {
    "Positive",
    "Negative",
    "Boundary",
    "Edge"
}


# ============================================================
# VALIDATE ONE TEST CASE
# ============================================================

def validate_test_case(test_case):

    errors = []


    if not isinstance(test_case, dict):

        return {
            "valid": False,
            "errors": [
                "Test case must be a JSON object."
            ]
        }


    # Check required fields

    for field in REQUIRED_TEST_FIELDS:

        if field not in test_case:

            errors.append(
                f"Missing required field: {field}"
            )


    # Check test steps

    if "test_steps" in test_case:

        if not isinstance(
            test_case["test_steps"],
            list
        ):

            errors.append(
                "test_steps must be a list."
            )


        elif len(
            test_case["test_steps"]
        ) == 0:

            errors.append(
                "test_steps cannot be empty."
            )


    # Check preconditions

    if "preconditions" in test_case:

        if not isinstance(
            test_case["preconditions"],
            list
        ):

            errors.append(
                "preconditions must be a list."
            )


    # Check expected result

    if "expected_result" in test_case:

        if not str(
            test_case["expected_result"]
        ).strip():

            errors.append(
                "expected_result cannot be empty."
            )


    # Check test type

    if "test_type" in test_case:

        if test_case["test_type"] not in (
            VALID_TEST_TYPES
        ):

            errors.append(
                "Invalid test_type: "
                f"{test_case['test_type']}"
            )


    # Check traceability

    if (
        "requirement_id" in test_case
        and
        "traceability" in test_case
    ):

        requirement_id = str(
            test_case["requirement_id"]
        )

        traceability = str(
            test_case["traceability"]
        )


        if requirement_id not in traceability:

            errors.append(
                "traceability must reference "
                "requirement_id."
            )


    return {
        "valid":
            len(errors) == 0,

        "errors":
            errors
    }


# ============================================================
# VALIDATE ALL TEST CASES
# ============================================================

def validate_test_cases(
    test_cases
):

    if not isinstance(
        test_cases,
        list
    ):

        return {
            "valid": False,
            "total": 0,
            "valid_count": 0,
            "invalid_count": 0,
            "errors": [
                "test_cases must be a list."
            ]
        }


    all_errors = []

    valid_count = 0


    for index, test_case in enumerate(
        test_cases,
        start=1
    ):

        result = validate_test_case(
            test_case
        )


        if result["valid"]:

            valid_count += 1

        else:

            for error in result["errors"]:

                all_errors.append(
                    f"Test case {index}: {error}"
                )


    return {
        "valid":
            len(all_errors) == 0,

        "total":
            len(test_cases),

        "valid_count":
            valid_count,

        "invalid_count":
            len(test_cases) - valid_count,

        "errors":
            all_errors
    }


# ============================================================
# ANALYZE TEST COVERAGE
# ============================================================

def analyze_coverage(
    test_cases
):

    coverage = {
        "Positive": 0,
        "Negative": 0,
        "Boundary": 0,
        "Edge": 0
    }


    for test_case in test_cases:

        test_type = test_case.get(
            "test_type"
        )


        if test_type in coverage:

            coverage[test_type] += 1


    total = len(test_cases)


    return {
        "total_test_cases":
            total,

        "test_type_counts":
            coverage,

        "positive_coverage":
            coverage["Positive"] > 0,

        "negative_coverage":
            coverage["Negative"] > 0,

        "boundary_coverage":
            coverage["Boundary"] > 0,

        "edge_coverage":
            coverage["Edge"] > 0
    }


# ============================================================
# FIND COVERAGE GAPS
# ============================================================

def find_coverage_gaps(
    test_cases
):

    gaps = []


    test_types = {
        test_case.get("test_type")
        for test_case in test_cases
    }


    if "Positive" not in test_types:

        gaps.append(
            "No Positive test case found."
        )


    if "Negative" not in test_types:

        gaps.append(
            "No Negative test case found."
        )


    if "Boundary" not in test_types:

        gaps.append(
            "No Boundary test case found."
        )


    if "Edge" not in test_types:

        gaps.append(
            "No Edge test case found."
        )


    return gaps


# ============================================================
# CHECK JSON STRUCTURE
# ============================================================

def check_json_structure(
    result
):

    if not isinstance(
        result,
        dict
    ):

        return {
            "passed": False,
            "score": 0,
            "message":
                "Output is not a JSON object."
        }


    test_cases = result.get(
        "test_cases"
    )


    if not isinstance(
        test_cases,
        list
    ):

        return {
            "passed": False,
            "score": 0,
            "message":
                "test_cases must be a list."
        }


    return {
        "passed": True,
        "score": 100,
        "message":
            "Valid JSON structure."
    }


# ============================================================
# CHECK REQUIRED FIELDS
# ============================================================

def check_required_fields(
    test_cases
):

    if not test_cases:

        return {
            "passed": False,
            "score": 0,
            "missing_fields": []
        }


    total_fields = (
        len(test_cases)
        *
        len(REQUIRED_TEST_FIELDS)
    )


    valid_fields = 0

    missing_fields = []


    for index, test_case in enumerate(
        test_cases
    ):

        for field in REQUIRED_TEST_FIELDS:

            if field in test_case:

                valid_fields += 1

            else:

                missing_fields.append(
                    f"Test case {index + 1}: "
                    f"missing {field}"
                )


    score = round(
        (
            valid_fields /
            total_fields
        )
        * 100,
        2
    )


    return {
        "passed":
            len(missing_fields) == 0,

        "score":
            score,

        "missing_fields":
            missing_fields
    }


# ============================================================
# CHECK TEST TYPE COVERAGE
# ============================================================

def check_test_type_coverage(
    test_cases
):

    actual_types = set()


    for test_case in test_cases:

        test_type = test_case.get(
            "test_type"
        )


        if test_type:

            actual_types.add(
                test_type
            )


    covered = (
        actual_types &
        VALID_TEST_TYPES
    )


    score = round(
        (
            len(covered) /
            len(VALID_TEST_TYPES)
        )
        * 100,
        2
    )


    return {
        "score":
            score,

        "covered_types":
            sorted(covered),

        "missing_types":
            sorted(
                VALID_TEST_TYPES -
                covered
            )
    }


# ============================================================
# CHECK REQUIREMENT COVERAGE
# ============================================================

def check_requirement_coverage(
    requirement,
    test_cases
):

    requirement_words = set(
        re.findall(
            r"\b[a-zA-Z]{4,}\b",
            requirement.lower()
        )
    )


    if not requirement_words:

        return {
            "score": 0,
            "matched_words": [],
            "message":
                "Requirement contains no useful keywords."
        }


    combined_text = " ".join(
        (
            str(
                test_case.get(
                    "requirement",
                    ""
                )
            )
            + " "
            +
            str(
                test_case.get(
                    "scenario",
                    ""
                )
            )
            + " "
            +
            str(
                test_case.get(
                    "expected_result",
                    ""
                )
            )
        )
        for test_case in test_cases
    ).lower()


    matched_words = [
        word
        for word in requirement_words
        if word in combined_text
    ]


    score = round(
        (
            len(matched_words) /
            len(requirement_words)
        )
        * 100,
        2
    )


    return {
        "score":
            score,

        "matched_words":
            matched_words,

        "total_requirement_keywords":
            len(requirement_words)
    }


# ============================================================
# CHECK TRACEABILITY
# ============================================================

def check_traceability(
    test_cases
):

    if not test_cases:

        return {
            "score": 0,
            "passed": False
        }


    valid = 0


    for test_case in test_cases:

        requirement_id = (
            test_case.get(
                "requirement_id"
            )
        )


        traceability = (
            test_case.get(
                "traceability"
            )
        )


        if (
            requirement_id
            and
            traceability
            and
            requirement_id in str(
                traceability
            )
        ):

            valid += 1


    score = round(
        (
            valid /
            len(test_cases)
        )
        * 100,
        2
    )


    return {
        "score":
            score,

        "passed":
            score == 100
    }


# ============================================================
# OVERALL AI TEST GENERATION EVALUATION
# ============================================================

def evaluate_test_generation(
    requirement,
    result
):

    test_cases = result.get(
        "test_cases",
        []
    )


    structure = check_json_structure(
        result
    )


    fields = check_required_fields(
        test_cases
    )


    types = check_test_type_coverage(
        test_cases
    )


    coverage = check_requirement_coverage(
        requirement,
        test_cases
    )


    traceability = check_traceability(
        test_cases
    )


    overall_score = round(
        (
            structure["score"]
            * 0.20

            +

            fields["score"]
            * 0.25

            +

            types["score"]
            * 0.20

            +

            coverage["score"]
            * 0.20

            +

            traceability["score"]
            * 0.15
        ),
        2
    )


    if overall_score >= 90:

        rating = "Excellent"

    elif overall_score >= 75:

        rating = "Good"

    elif overall_score >= 60:

        rating = "Needs Improvement"

    else:

        rating = "Poor"


    return {
        "overall_score":
            overall_score,

        "rating":
            rating,

        "metrics": {

            "json_structure":
                structure,

            "required_fields":
                fields,

            "test_type_coverage":
                types,

            "requirement_coverage":
                coverage,

            "traceability":
                traceability
        }
    }


# ============================================================
# QUICK SELF TEST
# ============================================================

if __name__ == "__main__":

    requirement = (
        "Users must provide a unique "
        "username during registration."
    )


    sample_test_cases = [

        {
            "test_case_id":
                "TC-001",

            "requirement_id":
                "REQ-001",

            "requirement":
                requirement,

            "scenario":
                "User registers with a "
                "unique username.",

            "test_type":
                "Positive",

            "priority":
                "High",

            "risk":
                "Medium",

            "preconditions": [
                "Registration page is available."
            ],

            "test_steps": [
                "Open registration page.",
                "Enter unique username.",
                "Submit registration."
            ],

            "test_data":
                "username=testuser123",

            "expected_result":
                "Registration succeeds.",

            "traceability":
                "REQ-001"
        }
    ]


    result = {
        "test_cases":
            sample_test_cases
    }


    print(
        "Validation:"
    )

    print(
        validate_test_cases(
            sample_test_cases
        )
    )


    print(
        "\nCoverage:"
    )

    print(
        analyze_coverage(
            sample_test_cases
        )
    )


    print(
        "\nCoverage gaps:"
    )

    print(
        find_coverage_gaps(
            sample_test_cases
        )
    )


    print(
        "\nEvaluation:"
    )

    print(
        evaluate_test_generation(
            requirement,
            result
        )
    )