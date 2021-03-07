import os
import time
import unittest
import configparser
from BeautifulReport import BeautifulReport

from utils import file
from utils import constants


def get_case_filename(execute_case_config_path=r".\config\testcase.ini", case_file_path=r".\test_cases"):
    """
    获取有效用例文件名
    :param execute_case_config_path: 用例执行范围的配置文件
    :param case_file_path: 读取用例的根目录
    :return: {"py_case_filename": [py文件名称,], "api_case_filename": [非py文件名称,]}
    """

    if not os.path.exists(execute_case_config_path):
        raise ValueError(f"用例配置文件 {execute_case_config_path} 在目录{os.getcwd()}中不存在，请确认！")

    if not os.path.exists(case_file_path):
        raise ValueError(f"用例根目录 {case_file_path} 在目录{os.getcwd()}中不存在，请确认！")

    case_files = file.read_file(execute_case_config_path).splitlines()
    # 分离配置文件中的py文件和非py文件
    py_case_filename = []
    api_case_filename = []

    not_exist_file = []
    for case_file in case_files:
        if case_file.startswith(";") or case_file.startswith("#") or case_file == "":
            continue
        file_path = file.find_file(case_file_path, case_file)
        if not file_path:
            not_exist_file.append(case_file)
        if case_file.endswith("py"):
            py_case_filename.append(case_file)
        else:
            api_case_filename.append(case_file)

    # 如果存在无效用例名，则抛错
    if not_exist_file:
        raise ValueError(f"这些用例文件{not_exist_file}不存在，请核实！")

    return {"py_case_filename": py_case_filename, "api_case_filename": api_case_filename}


def register_module(register_dir, py_filenames):
    """读取所有用例文件，并在用例根目录的__init__.py文件中注册模块"""

    # 注册文件为用例目录下__init__.py文件
    register_file = rf"{register_dir}\__init__.py"

    # 删除并注册模块
    file.delete_file(register_file)
    file.create_file(register_file)

    # 获取当前执行文件所在的目录
    project_name = file.get_path_last_name(os.getcwd())

    for py_filename in py_filenames:
        # 通过用例文件找到文件路径
        file_path = file.find_file(register_dir, py_filename)
        file_path = file_path.get(py_filename).split(project_name)[-1]

        # 从文件路径提取目录路径
        split_path = file_path.split("\\")
        split_path.remove(py_filename)
        split_path.remove("")

        # 拼接注册信息
        file_module = py_filename.split(".")[0]
        file_module_path = ".".join(split_path)
        register_msg = f"from {file_module_path} import {file_module}\n"

        # 注册用例模块
        file.append_write_file(register_file, register_msg)


def generate_pyfile_case_suite(py_filenames=None, testcase_start_dir="test_cases"):
    """
    将py文件中的用例添加到测试套
    :param testcase_start_dir: 测试用例的根目录，指的是项目目录下用例所在的目录
    :param py_filenames: 用例文件名称，list类型
    :return: 返回测试套
    """
    # 如果不指定用例编号，就把用例目录
    if py_filenames is None:
        # 将根目录用例添加到测试套
        suite = unittest.defaultTestLoader.discover(testcase_start_dir)
        return suite

    # 将用户输入的用例目录转换成绝对路径
    testcase_start_dir_abspath = os.path.abspath(testcase_start_dir)

    # 获取用例根目录的名称
    testcase_dir_name = file.get_path_last_name(testcase_start_dir_abspath)

    if not isinstance(py_filenames, list):
        raise ValueError(f"参数{py_filenames}不是list类型")

    if not os.path.exists(testcase_start_dir_abspath):
        raise ValueError(f"用例根目录 {testcase_dir_name} 在目录{os.getcwd()}中不存在，请确认用例根目录")

    # 根据py文件注册在根目录注册模块
    register_module(testcase_start_dir_abspath, py_filenames)

    # 将所有用例加载到测试套中
    suite = unittest.TestSuite()
    for py_filename in py_filenames:
        module_name = py_filename.split(".")[0]
        module_path = f"{testcase_dir_name}.{module_name}"
        suite.addTest(unittest.TestLoader().loadTestsFromName(module_path))
    return suite


def set_ddt_data(api_filenames):
    config = configparser.ConfigParser()
    config.clear()

    for api_filename in api_filenames:
        api_filepath = file.find_file(r".\test_cases", filename=api_filename).get(api_filename)
        config.read(api_filepath, encoding="utf-8")

    api_case_ids = config.sections()
    ddt_data = []
    for api_case_id in api_case_ids:
        case_info = {}
        case_info.setdefault("case_name", api_case_id)
        case_info.update(dict(config[api_case_id]))

        # 如果没有，就增加默认值
        case_info.setdefault("description", '')
        case_info.setdefault("method", "get")
        case_info.setdefault("headers", '')
        case_info.setdefault("data", '')
        case_info.setdefault("result_type", 'json')
        case_info.setdefault("expect_result", '')

        ddt_data.append(case_info)

    constants.DDT_DATA = ddt_data


def generate_api_case_suite(api_filenames=None, case_builder_path="utils.request_api"):
    set_ddt_data(api_filenames)
    suite = unittest.TestLoader().loadTestsFromName(case_builder_path)
    return suite


class Report(BeautifulReport):

    def generate_report(self, description, filename: str = None, report_dir=None, log_path=None, theme='theme_default'):
        if filename is None:
            time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
            filename = f"report_{time_str}"

        if report_dir is None:
            report_dir = r".\report"
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)

        self.report(description, filename, report_dir, log_path, theme)
