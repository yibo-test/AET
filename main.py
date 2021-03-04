import unittest
import time
from utils.unit_test import generate_unittest_suite, Report, get_ini_info

if __name__ == '__main__':
    # 分离配置文件中的py文件和非py文件
    py_ini_info = []
    other_ini_info = []
    for ini_info in get_ini_info():
        if ini_info.endswith(".py"):
            # 分离Py文件
            py_ini_info.append(ini_info)
        else:
            # 分离非py文件
            other_ini_info.append(ini_info)

    print(py_ini_info)
    print(other_ini_info)



    suite = generate_unittest_suite(testcase_start_dir=r".\test_cases", py_filenames=py_ini_info)

    # test_cases_dir = "test_cases/API"
    # suite = unittest.defaultTestLoader.discover(test_cases_dir)

    print(suite)
    #
    # # 2.提取BeautifulReport执行结果
    # runner = Report(suite)
    # runner.generate_report("基础用例", report_dir=r".\report", filename=r".\report.html")
