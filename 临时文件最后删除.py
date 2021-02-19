import unittest
import os
import sys


print(dir(unittest))

# unittest.main()

path = os.path.normpath("./test_cases")
sys.path.append(path)
name = "test_baidu"

suite = unittest.TestSuite()

# 方法1：获取module中的函数和方法引用
module = __import__(name)
module_attrs = dir(module)
print(module_attrs)
for module_attr in module_attrs:
    obj = getattr(module, module_attr)
    if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
        print(obj)
        ret = unittest.TestLoader().loadTestsFromTestCase(obj)
        print(ret)
        # suite.addTests(ret)

# print(suite)
# # 方法2：获取module中的函数和方法引用
# __import__(name)
# module = sys.modules[name]
# module_attrs = dir(module)
# for module_attr in module_attrs:
#     obj = getattr(module, module_attr)
#     if isinstance(obj, type):
#         print(obj)
