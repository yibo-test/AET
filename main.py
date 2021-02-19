import unittest
from utils.report import Report

# from test_cases.test_weather import WeatherTest
# from test_cases.test_fail_report import FailTest
# from test_cases.test_baidu import Baidu


if __name__ == '__main__':

    # 创建测试套1
    # # 将指定目录下所有以test开头的用例自动添加到测试套中
    # test_cases_dir = "./test_cases/"
    # suite = unittest.defaultTestLoader.discover(test_cases_dir, pattern='test*.py')

    # # 创建测试套2
    # suite = unittest.TestSuite()
    # # addTest 一次只能加一个用例
    # suite.addTest(WeatherTest("test_get_weather_info"))
    # # addTests 一次能添加多个用例，多个用例以列表传入
    # suite.addTests([WeatherTest("test_get_weather_info")])

    # 创建测试套3，通过用例路径导入用例，不需要导入模块
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromNames(["test_cases.test_weather.WeatherTest", "test_cases.test_fail_report.FailTest", "test_cases.test_baidu.Baidu"]))

    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(WeatherTest))

    # 执行测试并生成报告
    runner = Report(suite)
    runner.generate_report(description="基础用例")
