import unittest
from utils.unit_test import generate_unittest_suite, Report

if __name__ == '__main__':
    # # testcase_ids = ["weather.WeatherTest.test_get_weather_info", "test_fail_report.FailTest.test_sum_success"]
    testcase_ids = ["weather.WeatherTest.test_get_weather_info"]
    suite = generate_unittest_suite(testcase_ids)

    # test_cases_dir = "test_cases/API"
    # suite = unittest.defaultTestLoader.discover(test_cases_dir)

    print(suite)

    # 2.提取BeautifulReport执行结果
    runner = Report(suite)
    runner.generate_report("基础用例", report_dir=r".\report")
