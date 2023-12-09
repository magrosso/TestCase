from TestCase import TestCase


def test_case_1(test_name: str):
    with TestCase(test_name=test_name, execute_all=True) as tc:
        for num in range(10):
            tc.assert_equal(num % 2, 0, add_fail_message=f"{num} not even")
        tc.assert_equal(actual=3, expected=4)
