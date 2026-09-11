from app.evaluator import (
    check_json_structure,
    check_required_fields,
    check_test_type_coverage,
    validate_test_case,
    validate_test_cases
)


def test_json_structure():

    result = {
        "test_cases": []
    }

    evaluation = check_json_structure(
        result
    )

    assert evaluation["passed"] is True


def test_required_fields():

    test_case = {
        "test_case_id": "TC-001",
        "requirement_id": "REQ-001",
        "requirement": "User registration",
        "scenario": "Register valid user",
        "test_type": "Positive",
        "priority": "High",
        "risk": "Medium",
        "preconditions": [
            "Registration page is available."
        ],
        "test_steps": [
            "Open registration page.",
            "Enter valid username.",
            "Submit registration."
        ],
        "test_data": "username=testuser",
        "expected_result": "Registration succeeds.",
        "traceability": "REQ-001"
    }

    result = check_required_fields(
        [test_case]
    )

    assert result["passed"] is True


def test_test_type_coverage():

    test_cases = [
        {
            "test_type": "Positive"
        },
        {
            "test_type": "Negative"
        }
    ]

    result = check_test_type_coverage(
        test_cases
    )

    assert "Positive" in result[
        "covered_types"
    ]

    assert "Negative" in result[
        "covered_types"
    ]


def test_validate_test_case():

    test_case = {
        "test_case_id": "TC-001",
        "requirement_id": "REQ-001",
        "requirement": "User registration",
        "scenario": "Valid registration",
        "test_type": "Positive",
        "priority": "High",
        "risk": "Medium",
        "preconditions": [],
        "test_steps": [
            "Register user"
        ],
        "test_data": "valid user",
        "expected_result": "Registration succeeds.",
        "traceability": "REQ-001"
    }

    result = validate_test_case(
        test_case
    )

    assert result["valid"] is True


def test_validate_test_cases():

    test_case = {
        "test_case_id": "TC-001",
        "requirement_id": "REQ-001",
        "requirement": "User registration",
        "scenario": "Valid registration",
        "test_type": "Positive",
        "priority": "High",
        "risk": "Medium",
        "preconditions": [],
        "test_steps": [
            "Register user"
        ],
        "test_data": "valid user",
        "expected_result": "Registration succeeds.",
        "traceability": "REQ-001"
    }

    result = validate_test_cases(
        [test_case]
    )

    assert result["valid"] is True
    assert result["valid_count"] == 1