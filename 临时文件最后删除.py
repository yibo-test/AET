import os
import time
import unittest
from BeautifulReport import BeautifulReport

from utils import file


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
        project_path = file.get_path_last_name()

        # 如果不一致，找出未注册用例模块，并自动注册
        for file_module in exist_file_modules:
            if file_module not in import_module_names:
                # 通过用例模块找到文件路径
                filename = file_module + ".py"
                file_path = file.find_file(register_dir, filename)
                file_path = file_path.split(project_path)[-1]

                # 从文件路径提取目录路径
                split_path = file_path.split(".")[0].split("\\")
                split_path.remove(file_module)
                split_path.remove("")

                # 拼接注册信息
                file_module_path = ".".join(split_path)
                register_msg = f"from {file_module_path} import {file_module}\n"

                # 注册用例模块
                file.append_write_file(register_file, register_msg)