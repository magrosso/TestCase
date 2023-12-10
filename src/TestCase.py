from typing import Self


class TestCase:
    """A class to manage execution and result of a test case consisting of one or more assertions by means of a context manager.
    The simplest, which is generally also the best, test case has just a single assertion.
    In certain cases like slow test execution speed or increased complexity of test setup and teardown, single assertion test cases are not practical.
    This is typically the case for UI testing of Windows desktop applications.
    For those test scenarios, test cases usually are more complex containing more than a single assertion.
    This class provides some control over multi-assertion tests by allowing to defer a test failure until certain conditions are met, e.g.:
        1. Stop test case execution and fail test case after first failed assertion -> DEFAULT behaviour
        2. Execute all assertions first, then fail test case with summary of failed assertions
        3. Execute all assertions and fail test case if all assertions failed

    By keeping track of the individual assertion results of a test case, we are able to:
    - Decide if and how to stop the test case execution and
    - Decide if and when to raise an exception, e.g. in order to notify Frameworks like Robot Framework about the overall result of the test case

    Possible scenarios of how a test case with more than one assertion can fail:

    """

    def __init__(self, test_name: str, execute_all: bool = False, print_fail_summary: bool = False):
        self.results: list[tuple[bool, str | None]] = []
        self.test_name = test_name
        self.continue_on_failure = execute_all
        self.print_fail_summary = print_fail_summary

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # end of test case block reached or exception occurred inside test case block
        failed_results: list[str | None] = [result[1] for result in self.results if not result[0]]
        no_exception: tuple[bool, bool, bool] = (exc_type is None, exc_val is None, exc_tb is None)
        total_assert_count: int = len(self.results)
        failed_assert_count: int = len(failed_results)
        passed_assert_count: int = total_assert_count - failed_assert_count
        tc_fail_message: str = f"assertions failed={failed_assert_count},  passed={passed_assert_count}"
        if all(no_exception):
            # no exception during test case execution
            if failed_results:
                if self.print_fail_summary:
                    for failed_result_message in failed_results:
                        print(f"{failed_result_message}")
                raise AssertionError(f"{self.test_name} failed: {tc_fail_message}")
        else:
            # exception occurred during test case execution: log error and re-raise any exception
            print(f"{self.test_name} failed with Exception: {exc_val} ({tc_fail_message})")
            # re-raise any exception
            return False
        return True

    def assert_equal(
        self, actual: int, expected: int, assert_fail_message: str = "", force_test_fail: bool = False
    ) -> bool:
        assert_result: bool = actual == expected

        fail_message: str | None = (
            f"{self.test_name} - assert_equal({actual=} == {expected=}) failed ({assert_fail_message})"
            if not assert_result
            else None
        )
        return self._track_assert_result(
            assert_result=assert_result, fail_message=fail_message, force_test_fail=force_test_fail
        )

    def assert_is(
        self, actual: bool, expected: bool, assert_fail_message: str = "", force_test_fail: bool = False
    ) -> bool:
        assert_result: bool = actual is expected

        fail_message: str | None = (
            f"{self.test_name} - assert_is({actual=} is {expected=}) failed ({assert_fail_message})"
            if not assert_result
            else None
        )

        return self._track_assert_result(
            assert_result=assert_result, fail_message=fail_message, force_test_fail=force_test_fail
        )

    def _track_assert_result(self, assert_result: bool, fail_message: str | None, force_test_fail: bool) -> bool:
        # keep track of assert results within test case context
        self.results.append((assert_result, fail_message))

        # If assertion failed, either:
        # a. the whole test case fails immediately by raising an exception
        #    - force_test_fail is True or
        #    - continue_on_failure is False
        # b. or an error is logged:
        if not assert_result:
            if force_test_fail or not self.continue_on_failure:
                raise AssertionError(fail_message)
            print(f"Log Error: {fail_message}")

        return assert_result
