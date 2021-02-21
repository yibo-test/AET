from BeautifulReport import BeautifulReport
from utils.unit_test import generate_unittest_suite
from utils.report import Report


if __name__ == '__main__':
    # testcase_ids = ["weather.WeatherTest.test_get_weather_info", "test_fail_report.FailTest.test_sum_success"]
    testcase_ids = ["weather", "test_fail_report", "test_baidu"]
    suite = generate_unittest_suite(testcase_ids)

    # 2.提取BeautifulReport执行结果
    runner = Report(suite)
    runner.generate_report("基础用例")
