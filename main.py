import unittest
from utils.unit_test import generate_unittest_suite, Report
from test_cases import __manage_testcase__

if __name__ == '__main__':
    testcase_ids = __manage_testcase__.all_case
    suite = generate_unittest_suite(testcase_start_dir=r".\test_cases", testcase_ids=testcase_ids)

    # test_cases_dir = "test_cases/API"
    # suite = unittest.defaultTestLoader.discover(test_cases_dir)

    print(suite)

    # 2.提取BeautifulReport执行结果
    runner = Report(suite)
    runner.generate_report("基础用例", report_dir=r".\report")
