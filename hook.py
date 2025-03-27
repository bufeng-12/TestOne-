def before_all(params):
    print(f"Before all tests: {params}")


def after_all(test_results, params):
    passed_count = sum(1 for result in test_results if result['result'])
    failed_count = len(test_results) - passed_count
    print(f"After all tests: Passed {passed_count}, Failed {failed_count}, Params: {params}")
    