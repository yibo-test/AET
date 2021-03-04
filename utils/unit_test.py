import os
import time
import unittest
from BeautifulReport import BeautifulReport

from utils import file


def get_ini_info():
    _ids = file.read_file("./config/testcase.ini").splitlines()
    new_ids = []
    for _id in _ids:
        if _id.startswith(";") or _id.startswith("#") or _id == "":
            continue
        new_ids.append(_id)
    return new_ids


def register_module(register_dir, testcase_ids):
    # 根据用例id，获取所有用例的模块名称
    exist_file_modules = []
    not_exist_file_module = []
    for testcase_id in testcase_ids:
        file_module = testcase_id.split(".")[0]
        # 根据文件名称查找文件，若不存在则反None
        filename = file_module + ".py"
        file_path = file.find_file(register_dir, filename)
        if file_path:
            exist_file_modules.append(file_module)
        else:
            not_exist_file_module.append(file_module)

    # 校验是否存在没有用例文件的模块
    if not_exist_file_module:
        raise ValueError(f"这些用例模块{not_exist_file_module}不存在用例文件，请核实！")

    # 注册文件为用例目录下__init__.py文件
    register_file = rf"{register_dir}\__init__.py"

    # 校验注册文件存不存在，不存在就创建
    file.create_file(register_file)

    # 获取已注册的用例模块
    import_module_names = []
    msg = file.read_file(register_file)
    for line in msg.splitlines():
        name = line.split(" ")[-1]
        import_module_names.append(name)

    # 对列表进行排序，并校验两个列表是否相等
    exist_file_modules.sort()
    import_module_names.sort()
    if exist_file_modules != import_module_names:
        # 当前执行文件所在的目录名称
        project_name = file.get_path_last_name()

        # 如果不一致，找出未注册用例模块，并自动注册
        for file_module in exist_file_modules:
            if file_module not in import_module_names:
                # 通过用例模块找到文件路径
                filename = file_module + ".py"
                file_path = file.find_file(register_dir, filename)
                file_path = file_path.get(filename).split(project_name)[-1]

                # 从文件路径提取目录路径
                split_path = file_path.split(".")[0].split("\\")
                split_path.remove(file_module)
                split_path.remove("")

                # 拼接注册信息
                file_module_path = ".".join(split_path)
                register_msg = f"from {file_module_path} import {file_module}\n"

                # 注册用例模块
                file.append_write_file(register_file, register_msg)


def generate_unittest_suite(testcase_start_dir="test_cases", py_filenames=None):
    """
    把testcase_ids中的模块加载到测试套中
    :param py_filenames: 用例文件，list类型,用例id的格式为 module[.class[.method]]，中括号中缺省
    :param testcase_start_dir: 测试用例的根目录，指的是项目目录下用例所在的目录
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

    # 根据用例注册在根目录注册模块
    register_module(testcase_start_dir_abspath, py_filenames)

    # 将所有用例加载到测试套中
    suite = unittest.TestSuite()
    for py_filename in py_filenames:
        if py_filename.endswith(".py"):
            py_filename = py_filename.split(".")[0]
        py_filename = f"{testcase_dir_name}.{py_filename}"
        suite.addTest(unittest.TestLoader().loadTestsFromName(py_filename))
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
