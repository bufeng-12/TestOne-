def pretest(params, testbed):
    # 参数初始化
    global para_a
    para_a = params.get('para_a', 0)
    print(f"Pretest: Initialized para_a to {para_a}")


def testprocedure(params, testbed):
    # 测试用例的完成过程
    assert int(para_a) > 0, "para_a should be greater than 0"
    print("Test procedure passed.")


def aftertest(params, testbed):
    # 测试后续过程的处理
    print("Aftertest: Cleaning up environment and saving logs.")
    