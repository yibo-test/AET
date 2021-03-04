import configparser
from utils.file import find_file

conf = configparser.ConfigParser()
conf.clear()

file = list(find_file(r".\test_cases", file_endswith="ini").values())[0]
conf.read(file, encoding="utf-8")
sections = conf.sections()

test_case_info = {}
for section in sections:
    value = dict(conf[section])
    test_case_info.setdefault(section, value)
print(test_case_info)