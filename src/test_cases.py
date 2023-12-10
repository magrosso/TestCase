from TestCase import TestCase


def test_case_1(test_name: str):
    with TestCase(test_name=test_name, execute_all=True) as tc:
        for num in range(10):
            tc.assert_equal(num % 2, 0, assert_fail_message=f"{num} not even")
        tc.assert_equal(actual=3, expected=4)


def test_case_2(test_name: str):
    with TestCase(test_name=test_name) as tc:
        for num in range(12):
            tc.assert_is(actual=num % 2 == 0, expected=True, assert_fail_message=f"{num} is not even")
