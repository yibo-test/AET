import os


def find_file(search_path, find_filename, abspath=False) -> str:
    """
    查找指定目录下指定文件的路径
    :param search_path: 查找的目录路径
    :param find_filename: 查找的文件名称
    :param abspath: 是否返回绝对路径，默认返回相对路径
    :return: 返回文件的路径
    """
    # 是否返回绝对路径
    if abspath:
        search_path = os.path.abspath(search_path)

    filenames = os.listdir(search_path)
    if find_filename in filenames:
        return os.path.join(search_path, find_filename)

    for filename in filenames:
        child_path = os.path.join(search_path, filename)
        if os.path.isdir(child_path) and not (filename.startswith("__") and filename.endswith("__")):
            # 在子目录搜索
            ret = find_file(child_path, find_filename, abspath)
            if ret:
                return ret


def find_files(search_path, abspath=False, file_endswith=None) -> dict:
    """
    查找指定目录下所有的文件或指定格式的文件，若不同目录存在相同文件名，只返回第1个文件的路径
    :param search_path: 查找的目录路径
    :param abspath: 是否返回绝对路径，默认返回相对路径
    :param file_endswith: 指定搜索文件的格式，不指定默认搜索所有文件
    :return: 返回dict类型，key为文件名，value为文件路径
    """
    filename_filepath = {}
    if abspath:
        search_path = os.path.abspath(search_path)

    def __find_file(_search_path):
        filenames = os.listdir(_search_path)
        for filename in filenames:
            child_path = os.path.join(_search_path, filename)
            # 如果是文件就保存
            if os.path.isfile(child_path):
                if file_endswith is None:
                    filename_filepath.setdefault(filename, child_path)
                # 保存指定类型文件
                elif file_endswith is not None and child_path.endswith(file_endswith):
                    filename_filepath.setdefault(filename, child_path)
                continue

            # 如果目录且不是__开头和结尾，则继续查找
            if os.path.isdir(child_path) and not (filename.startswith("__") and filename.endswith("__")):
                __find_file(child_path)
    __find_file(search_path)
    return filename_filepath


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


def read_file(file) -> str:
    with open(file, "r", encoding="utf-8") as f:
        msg = f.read()
    return msg


def readline_file(file) -> list:
    with open(file, "r", encoding="utf-8") as f:
        msg = f.read().splitlines()
    return msg


def cover_write_file(file, msg):
    with open(file, "w") as f:
        f.write(msg)


def append_write_file(file, msg):
    with open(file, "a") as f:
        f.write(msg)
