from test_cases import test_case_1, test_case_2


def main() -> None:
    try:
        test_case_1(test_name="TC1")
    except AssertionError as ex:
        print(f"main: {ex}")
    try:
        test_case_2(test_name="TC2")
    except AssertionError as ex:
        print(f"main: {ex}")


if __name__ == "__main__":
    main()
