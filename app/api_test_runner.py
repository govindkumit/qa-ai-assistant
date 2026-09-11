import requests


DEFAULT_TIMEOUT = 5


def execute_api_test(
    test_case,
    timeout=DEFAULT_TIMEOUT
):
    """
    Execute one API test case safely.
    """

    method = test_case.get(
        "method",
        "GET"
    ).upper()

    url = test_case.get(
        "url"
    )

    if not url:

        return {
            "test_case_id":
                test_case.get("test_case_id"),

            "name":
                test_case.get("name"),

            "passed": False,

            "error":
                "API URL is missing."
        }


    headers = (
        test_case.get("headers")
        or {}
    )


    query_params = (
        test_case.get("query_params")
        or {}
    )


    body = test_case.get(
        "body"
    )


    expected_status = test_case.get(
        "expected_status"
    )


    try:

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=query_params,
            json=body,
            timeout=timeout
        )


        status_passed = (
            response.status_code ==
            expected_status
        )


        expected_values = (
            test_case.get(
                "expected_response_contains"
            )
            or []
        )


        response_text = response.text


        response_content_passed = all(
            str(value) in response_text
            for value in expected_values
        )


        passed = (
            status_passed
            and
            response_content_passed
        )


        return {
            "test_case_id":
                test_case.get(
                    "test_case_id"
                ),

            "name":
                test_case.get(
                    "name"
                ),

            "method":
                method,

            "url":
                url,

            "expected_status":
                expected_status,

            "actual_status":
                response.status_code,

            "status_check":
                status_passed,

            "response_check":
                response_content_passed,

            "passed":
                passed,

            "response_time_ms":
                round(
                    response.elapsed.total_seconds()
                    * 1000,
                    2
                ),

            "response_preview":
                response.text[:500]
        }


    except requests.exceptions.Timeout:

        return {
            "test_case_id":
                test_case.get(
                    "test_case_id"
                ),

            "name":
                test_case.get(
                    "name"
                ),

            "method":
                method,

            "url":
                url,

            "passed":
                False,

            "error":
                f"Request timed out after {timeout} seconds."
        }


    except requests.exceptions.RequestException as error:

        return {
            "test_case_id":
                test_case.get(
                    "test_case_id"
                ),

            "name":
                test_case.get(
                    "name"
                ),

            "method":
                method,

            "url":
                url,

            "passed":
                False,

            "error":
                str(error)
        }


    except Exception as error:

        return {
            "test_case_id":
                test_case.get(
                    "test_case_id"
                ),

            "name":
                test_case.get(
                    "name"
                ),

            "method":
                method,

            "url":
                url,

            "passed":
                False,

            "error":
                str(error)
        }


def execute_api_tests(
    test_cases
):

    # Safety limit
    test_cases = test_cases[:5]


    results = []


    for test_case in test_cases:

        result = execute_api_test(
            test_case
        )

        results.append(
            result
        )


    total = len(results)


    passed = sum(
        1
        for result in results
        if result.get("passed")
    )


    failed = (
        total - passed
    )


    return {
        "total": total,

        "passed": passed,

        "failed": failed,

        "results": results
    }


if __name__ == "__main__":

    test_cases = [

        {
            "test_case_id":
                "API-TC-001",

            "name":
                "Get valid user",

            "method":
                "GET",

            "url":
                "https://jsonplaceholder.typicode.com/users/1",

            "headers": {},

            "query_params": {},

            "body": None,

            "expected_status": 200,

            "expected_response_contains": [
                "id"
            ]
        }
    ]


    result = execute_api_tests(
        test_cases
    )


    print("\n")
    print("=" * 70)
    print("API TEST EXECUTION")
    print("=" * 70)


    print(
        result
    )