import unittest
from BeautifulReport import BeautifulReport

if __name__ == '__main__':

    # ==================================
    # =========== 创建测试套 ============
    # ==================================
    # # 创建测试套1：识别指定目录下所有以test开头的文件以及文件中的用例，并将用例自动添加到测试套中
    # test_cases_dir = "./test_cases/"
    # suite = unittest.defaultTestLoader.discover(test_cases_dir)
    # print(suite)

    # # 创建测试套2：添加指定用例（用例可以不以test开头，执行顺序为添加顺序）
    # suite = unittest.TestSuite()
    # # addTest 一次只能加一个用例
    # suite.addTest(WeatherTest("test_get_weather_info"))
    # # addTests 一次能添加多个用例，多个用例以列表传入
    # suite.addTests([WeatherTest("test_get_weather_info")])
    # print(suite)

    # 创建测试套3，以执行文件为参考，以相对路径的方式导入用例类，不需要导入模块
    suite = unittest.TestLoader().loadTestsFromNames(["test_cases.API.weather.WeatherTest", "test_cases.API.test_fail_report.FailTest"])

    # # 创建测试套4：将指定测试类下所有以test开头的用例添加到测试套中
    # suite = unittest.TestLoader().loadTestsFromTestCase(WeatherTest)

    # # # 创建测试套5：将指定模块中所有以test开头的用例添加到测试套中
    # path = os.path.normpath("./test_cases")
    # sys.path.append(path)
    # name = "weather"
    # module = __import__(name)
    # suite1 = unittest.TestLoader().loadTestsFromModule(module)
    # # 测试套中可以嵌套测试套
    # suite = unittest.TestSuite()
    # suite.addTests([suite1])
    # print(suite)

    # ==================================
    # =========== 执行用例 ==============
    # ==================================
    # # 1、简单的执行用例
    # # runner = unittest.TextTestRunner(verbosity=2)
    # # runner.run(suite)

    # # 2、使用BeautifulReport执行测试并生成报告
    # runner = BeautifulReport(suite)
    # runner.report("基础用例")

    # ==================================
    # =========== 提取测试结果 ==========
    # ==================================
    # # 1. 提取unittest的执行结果
    # runner = unittest.TextTestRunner(verbosity=2)
    # ret = runner.run(suite)
    # print(dir(ret))
    #
    # # 当所有用例执行成功后，返回True，否则返回False
    # print(ret.wasSuccessful())
    #
    # # 执行用例数
    # print(f"总用例数：{ret.testsRun}")
    #
    # # 失败用例结构f
    # fail_cases = ret.failures
    # print(f"失败用例数：{len(fail_cases)}")
    # for fail_case, fail_reason in fail_cases:
    #     print(f"用例id:{fail_case.id()}")
    #     print(f"用例失败原因：\n{fail_reason}")
    #
    # # 异常用例结果
    # error_cases = ret.errors
    # print(f"错误用例数：{len(error_cases)}")
    # for error_case, error_reason in error_cases:
    #     print(f"用例id:{error_case.id()}")
    #     print(f"用例失败原因：\n{error_reason}")

    # 2.提取BeautifulReport执行结果
    runner = BeautifulReport(suite)
    runner.report("基础用例")
    ret = runner.fields
    print(ret)
