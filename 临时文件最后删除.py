import os

def find_file(search_path, file_type="file", filename=None, file_endswith=None, abspath=False) -> dict:
    """
    查找指定目录下所有的文件（不包含以__开头和结尾的文件）或指定格式的文件，若不同目录存在相同文件名，只返回第1个文件的路径
    :param search_path: 查找的目录路径
    :param filename: 查找的目录或文件的名称，如果为none则查找所有
    :param abspath: 是否返回绝对路径，默认返回相对路径
    :param file_endswith: 指定搜索文件的格式，不指定默认搜索所有文件
    :return: 返回dict类型，key为文件名，value为文件路径
    """
    filename_path = {}
    the_filename_path = {}

    if abspath:
        search_path = os.path.abspath(search_path)

    def __find_file(_search_path):
        # 返回目录所有名称
        names = os.listdir(_search_path)
        find_flag = False

        # 如果查找指定文件，找到就停止查找
        if filename is not None and (filename in names):
            path = os.path.join(_search_path, filename)
            the_filename_path.setdefault(filename, path)
            find_flag = True
            return find_flag

        # 如果根目录未找到，在子目录继续查找
        for name in names:
            # 过滤以__开头并结尾的目录
            if name.startswith("__") and name.endswith("__"):
                continue

            child_path = os.path.join(_search_path, name)

            # 如果是文件就保存
            if file_type == "file" and os.path.isfile(child_path) and name != "__init__.py":
                if file_endswith is None:
                    filename_path.setdefault(name, child_path)
                # 保存指定格式的文件
                elif file_endswith is not None and child_path.endswith(file_endswith):
                    filename_path.setdefault(name, child_path)
                continue
            if os.path.isdir(child_path):
                if file_type == "dir":
                    filename_path.setdefault(name, child_path)
                _result = __find_file(child_path)
                if _result is True:
                    return _result

    result = __find_file(search_path)
    if filename is None:
        return filename_path

    if filename is not None:
        if result is True:
            return the_filename_path


if __name__ == '__main__':
    start_path = r".\test_cases"
    # 查找所有文件或目录
    ret = find_file(start_path, file_type="file")
    print(f'查找所有文件(file_type可缺省)：%s' % ret)
    ret = find_file(start_path, file_type="dir")
    print("查找所有目录：%s" % ret)

    # 查找指定文件或目录
    ret = find_file(start_path, file_type="dir", filename="asd")
    print("查找不存在的目录：%s" % ret)
    ret = find_file(start_path, file_type="dir", filename="weather.py")
    print("查找存在的文件名：%s" % ret)

    ret = find_file(start_path, file_type="file", filename="asd.py")
    print("查找不存的文件名：%s" % ret)


