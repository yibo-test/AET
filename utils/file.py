import os


def find_file(search_path, filename=None, file_type="file", file_startswith=None, file_endswith=None, abspath=False) -> dict:
    """
    查找指定目录下所有的文件（不包含以__开头和结尾的文件）或指定格式的文件，若不同目录存在相同文件名，只返回第1个文件的路径
    :param search_path: 查找的目录路径
    :param file_type: 查找的类型，可缺省，缺省则默认查找文件类型，可输入值：file和dir,file表示文件,dir表示目录
    :param filename: 查找名称，精确匹配，可缺省，缺省则返回所有文件或目录，不可与file_startswith或file_endswith组合使用
    :param file_startswith: 模糊匹配开头，可缺省，缺省则不匹配,可与file_endswith组合使用
    :param file_endswith:  模糊匹配结尾，可缺省，缺省则不匹配
    :param abspath: 是否返回绝对路径，默认返回相对路径
    :return: 返回dict类型，key为文件名，value为文件路径
    """
    filename_path = {}
    the_filename_path = {}

    if abspath:
        search_path = os.path.abspath(search_path)

    if file_type not in ["file", "dir"]:
        raise ValueError(f"file_type只能为file或dir，而输入值为{file_type}")

    def __find_file(_search_path):
        # 返回目录所有名称
        names = os.listdir(_search_path)
        find_flag = False

        # 如果查找指定文件，找到就停止查找
        if filename is not None and (filename in names):
            path = os.path.join(_search_path, filename)
            if file_type == "file" and os.path.isfile(path):
                the_filename_path.setdefault(filename, path)
                find_flag = True
            elif file_type == "dir" and os.path.isdir(path):
                the_filename_path.setdefault(filename, path)
                find_flag = True
            return find_flag

        # 如果根目录未找到，在子目录继续查找
        for name in names:
            # 过滤以__开头和__结尾的目录，以及__init__.py文件
            if name.startswith("__") and name.endswith("__") or name == "__init__.py":
                continue

            child_path = os.path.join(_search_path, name)

            # 如果是文件就保存
            if file_type == "file" and os.path.isfile(child_path):
                if file_startswith is None and file_endswith is None:
                    filename_path.setdefault(name, child_path)
                # 保存指定结尾的文件
                elif file_startswith is not None and file_endswith is None and name.startswith(file_startswith):
                    filename_path.setdefault(name, child_path)
                elif file_startswith is None and file_endswith is not None and name.endswith(file_endswith):
                    filename_path.setdefault(name, child_path)
                elif file_startswith is not None and file_endswith is not None and name.startswith(file_startswith) and name.endswith(file_endswith):
                    filename_path.setdefault(name, child_path)
                continue
            if os.path.isdir(child_path):
                if file_type == "dir":
                    if file_startswith is None and file_endswith is None:
                        filename_path.setdefault(name, child_path)
                    # 保存指定结尾的文件
                    elif file_startswith is not None and file_endswith is None and name.startswith(file_startswith):
                        filename_path.setdefault(name, child_path)
                    elif file_startswith is None and file_endswith is not None and name.endswith(file_endswith):
                        filename_path.setdefault(name, child_path)
                    elif file_startswith is not None and file_endswith is not None and name.startswith(file_startswith) and name.endswith(file_endswith):
                        filename_path.setdefault(name, child_path)

                _result = __find_file(child_path)
                if _result is True:
                    return _result

    result = __find_file(search_path)
    if filename is None:
        if filename_path:
            return filename_path

    if filename is not None:
        if result is True:
            return the_filename_path


def get_path_last_name(path=None):
    """
    获取path最后一个名称，如果不传值，则获取当前执行的所在目录
    :return:
    """
    if path is None:
        path = os.getcwd()
    return path.split("\\")[-1]


def create_file(file):
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            pass


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)


def read_file(file) -> str:
    with open(file, "r", encoding="utf-8") as f:
        msg = f.read()
    return msg


def cover_write_file(file, msg):
    with open(file, "w") as f:
        f.write(msg)


def append_write_file(file, msg):
    with open(file, "a") as f:
        f.write(msg)

