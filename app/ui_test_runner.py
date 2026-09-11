from pathlib import Path

from playwright.sync_api import (
    sync_playwright
)


SCREENSHOT_DIR = Path(
    "data/screenshots"
)


def execute_ui_test(
    test_case,
    headless=True
):

    SCREENSHOT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    test_case_id = test_case.get(
        "test_case_id",
        "unknown"
    )


    name = test_case.get(
        "name",
        "Unnamed test"
    )


    actions = test_case.get(
        "actions",
        []
    )


    screenshot_path = (
        SCREENSHOT_DIR /
        f"{test_case_id}.png"
    )


    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=headless
            )


            page = browser.new_page()


            for action in actions:

                action_type = action.get(
                    "action"
                )

                locator = action.get(
                    "locator",
                    ""
                )

                value = action.get(
                    "value",
                    ""
                )


                if action_type == "navigate":

                    page.goto(
                        value,
                        wait_until="domcontentloaded",
                        timeout=10000
                    )


                elif action_type == "click":

                    page.locator(
                        locator
                    ).click(
                        timeout=5000
                    )


                elif action_type == "fill":

                    page.locator(
                        locator
                    ).fill(
                        value,
                        timeout=5000
                    )


                elif action_type == "press":

                    page.locator(
                        locator
                    ).press(
                        value,
                        timeout=5000
                    )


            browser.close()


        return {
            "test_case_id":
                test_case_id,

            "name":
                name,

            "passed":
                True,

            "screenshot":
                None,

            "error":
                None
        }


    except Exception as error:

        try:

            with sync_playwright() as p:

                browser = p.chromium.launch(
                    headless=headless
                )

                page = browser.new_page()

                url = test_case.get(
                    "url"
                )

                if url:

                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=10000
                    )


                page.screenshot(
                    path=str(
                        screenshot_path
                    ),
                    full_page=True
                )


                browser.close()

        except Exception:
            pass


        return {
            "test_case_id":
                test_case_id,

            "name":
                name,

            "passed":
                False,

            "screenshot":
                str(
                    screenshot_path
                ),

            "error":
                str(error)
        }


def execute_ui_tests(
    test_cases,
    headless=True
):

    test_cases = test_cases[:5]


    results = []


    for test_case in test_cases:

        result = execute_ui_test(
            test_case,
            headless=headless
        )

        results.append(
            result
        )


    total = len(
        results
    )


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
                "UI-TC-001",

            "name":
                "Verify Example Domain",

            "test_type":
                "Positive",

            "url":
                "https://example.com",

            "actions": [

                {
                    "action":
                        "navigate",

                    "locator":
                        "",

                    "value":
                        "https://example.com"
                }
            ],

            "expected_result":
                "Example Domain is displayed."
        }
    ]


    result = execute_ui_tests(
        test_cases
    )


    print("\n")
    print("=" * 70)
    print("PLAYWRIGHT UI EXECUTION")
    print("=" * 70)


    print(result)