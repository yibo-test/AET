import unittest
from utils import unit_test


def run():
    # 读取用例配置文件中的信息
    dict_case_filename = unit_test.get_case_filename(execute_case_config_path=r".\config\testcase.ini", case_file_path=r".\test_cases")

    # 获取py文件类型，并生成测试套
    py_filenames = dict_case_filename.get("py_case_filename")
    py_suite = unit_test.generate_pyfile_case_suite(py_filenames=py_filenames)

    # 获取非py文件类型，并生成测试套
    api_filenames = dict_case_filename.get("api_case_filename")
    api_suite = unit_test.generate_api_case_suite(api_filenames=api_filenames)

    # 将两个测试套合成一个
    suite = unittest.TestSuite()
    suite.addTests([py_suite, api_suite])

    # 执行测试套并生成报告
    runner = unit_test.Report(suite)
    runner.generate_report("演示用例", report_dir=r".\report", filename=r".\report.html")
