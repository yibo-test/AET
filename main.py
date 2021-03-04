import unittest
import time
from utils.unit_test import generate_pyfile_case_suite, Report, get_case_filename,generate_api_case_suite

if __name__ == '__main__':
    # 读取用例配置文件中的信息
    dict_case_filename = get_case_filename(config_path=r".\config\testcase.ini", case_file_path=r".\test_cases")

    # 获取py文件类型，并生成测试套
    py_filenames = dict_case_filename.get("py_case_filename")
    py_suite = generate_pyfile_case_suite(testcase_start_dir=r".\test_cases", py_filenames=py_filenames)

    # 获取非py文件类型，并生成测试套
    api_case = dict_case_filename.get("api_case_filename")
    ...解析用例文件中的用例
    api_suite = generate_api_case_suite(api_demo_id_path="utils.api_demo")

    # 将两个测试套合成一个
    suite = unittest.TestSuite()
    suite.addTests([py_suite, api_suite])

    #
    # 2.提取BeautifulReport执行结果
    runner = Report(suite)
    runner.generate_report("基础用例", report_dir=r".\report", filename=r".\report.html")
