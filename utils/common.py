import os


def find_file_path(path, find_filename, abspath=False) -> str:
    """
    查找指定目录下指定文件的路径
    :param path: 查找的目录路径
    :param find_filename: 查找的文件名称
    :param abspath: 是否返回绝对路径，默认返回相对路径
    :return: 返回文件的路径
    """
    if abspath:
        path = os.path.abspath(path)

    if not find_filename.endswith(".py"):
        find_filename = find_filename + ".py"

    filenames = os.listdir(path)
    if find_filename in filenames:
        return os.path.join(path, find_filename)

    for filename in filenames:
        child_path = os.path.join(path, filename)
        if os.path.isdir(child_path) and not (filename.startswith("__") and filename.endswith("__")):
            ret = find_file_path(child_path, find_filename, abspath)
            if ret:
                return ret


def get_path_last_name(path=None):
    """
    获取path最后一个名称，如果不传值，则获取当前执行的所在目录
    :return:
    """
    if path is None:
        path = os.getcwd()
    return path.split("\\")[-1]



