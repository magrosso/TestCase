from test_cases import test_case_1


def main() -> None:
    tc_name: str = "TC 1"
    try:
        test_case_1(test_name=tc_name)
    except AssertionError as ex:
        print(ex)


if __name__ == "__main__":
    main()
