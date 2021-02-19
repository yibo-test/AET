import os, sys
import unittest
from utils.report import Report

from test_cases.weather import WeatherTest
from test_cases.test_fail_report import FailTest
from test_cases.test_baidu import Baidu


if __name__ == '__main__':

    # # 创建测试套1：识别指定目录下所有以test开头的目录和文件以及文件中的用例，并将用例自动添加到测试套中
    # test_cases_dir = "./test_cases/"
    # suite = unittest.defaultTestLoader.discover(test_cases_dir)
    # print(suite)

    # # 创建测试套2：添加指定用例（用例可以不以test开头）
    # suite = unittest.TestSuite()
    # # addTest 一次只能加一个用例
    # suite.addTest(WeatherTest("test_get_weather_info"))
    # # addTests 一次能添加多个用例，多个用例以列表传入
    # suite.addTests([WeatherTest("test_get_weather_info")])
    # print(suite)

    # 创建测试套3，以执行文件为参考，以相对路径的方式导入用例类，不需要导入模块
    # suite = unittest.TestLoader().loadTestsFromNames(["test_cases.test_weather.WeatherTest", "test_cases.test_fail_report.FailTest"])

    # # 创建测试套4：将指定类下所有以test开头的用例添加到测试套中
    # suite = unittest.TestLoader().loadTestsFromTestCase(WeatherTest)

    # 创建测试套5：将指定模块中所有以test开头的用例添加到测试套中
    path = os.path.normpath("./test_cases")
    sys.path.append(path)
    name = "weather"
    module = __import__(name)
    suite = unittest.TestLoader().loadTestsFromModule(module)
    # 测试套中可以嵌套加测试套
    suite1 = unittest.TestSuite()
    suite1.addTests([suite])
    print(suite1)

    # 执行测试并生成报告
    runner = Report(suite1)
    runner.generate_report(description="基础用例")
