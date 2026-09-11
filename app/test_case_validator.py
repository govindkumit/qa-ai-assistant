REQUIRED_FIELDS = [
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


VALID_PRIORITIES = {
    "High",
    "Medium",
    "Low"
}


VALID_RISKS = {
    "High",
    "Medium",
    "Low"
}


def validate_test_case(test_case):

    errors = []

    # -----------------------------------------
    # Required fields
    # -----------------------------------------

    for field in REQUIRED_FIELDS:

        if field not in test_case:

            errors.append(
                f"Missing field: {field}"
            )


    # Stop if basic structure is invalid
    if errors:
        return {
            "valid": False,
            "errors": errors
        }


    # -----------------------------------------
    # Test type
    # -----------------------------------------

    if test_case["test_type"] not in VALID_TEST_TYPES:

        errors.append(
            "Invalid test_type: "
            f"{test_case['test_type']}"
        )


    # -----------------------------------------
    # Priority
    # -----------------------------------------

    if test_case["priority"] not in VALID_PRIORITIES:

        errors.append(
            "Invalid priority: "
            f"{test_case['priority']}"
        )


    # -----------------------------------------
    # Risk
    # -----------------------------------------

    if test_case["risk"] not in VALID_RISKS:

        errors.append(
            "Invalid risk: "
            f"{test_case['risk']}"
        )


    # -----------------------------------------
    # Preconditions
    # -----------------------------------------

    if not isinstance(
        test_case["preconditions"],
        list
    ):

        errors.append(
            "preconditions must be a list"
        )


    # -----------------------------------------
    # Test steps
    # -----------------------------------------

    if not isinstance(
        test_case["test_steps"],
        list
    ):

        errors.append(
            "test_steps must be a list"
        )

    elif len(
        test_case["test_steps"]
    ) == 0:

        errors.append(
            "test_steps cannot be empty"
        )


    # -----------------------------------------
    # Expected result
    # -----------------------------------------

    if not str(
        test_case["expected_result"]
    ).strip():

        errors.append(
            "expected_result cannot be empty"
        )


    # -----------------------------------------
    # Traceability
    # -----------------------------------------

    if not str(
        test_case["traceability"]
    ).strip():

        errors.append(
            "traceability cannot be empty"
        )


    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_test_cases(test_cases):

    results = []

    valid_count = 0

    invalid_count = 0

    for test_case in test_cases:

        validation = validate_test_case(
            test_case
        )

        result = {
            "test_case_id": test_case.get(
                "test_case_id",
                "UNKNOWN"
            ),
            "valid": validation["valid"],
            "errors": validation["errors"]
        }

        results.append(result)

        if validation["valid"]:

            valid_count += 1

        else:

            invalid_count += 1


    return {
        "total": len(test_cases),
        "valid": valid_count,
        "invalid": invalid_count,
        "results": results
    }


if __name__ == "__main__":

    sample_test_case = {
        "test_case_id": "TC-001",
        "requirement_id": "REQ-001",
        "requirement": (
            "Username must be unique."
        ),
        "scenario": (
            "Register using a unique username."
        ),
        "test_type": "Positive",
        "priority": "High",
        "risk": "High",
        "preconditions": [
            "Registration page is available."
        ],
        "test_steps": [
            "Enter a unique username.",
            "Enter valid registration data.",
            "Submit the registration form."
        ],
        "test_data": (
            "username=testuser123"
        ),
        "expected_result": (
            "Registration succeeds."
        ),
        "traceability": "REQ-001"
    }


    result = validate_test_case(
        sample_test_case
    )


    print(
        "Validation result:"
    )

    print(result)