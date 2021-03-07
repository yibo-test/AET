import unittest
import logging
from libs import ddt
import requests
import json
from utils.constants import DDT_DATA
from json.decoder import JSONDecodeError


@ddt.ddt
class Api(unittest.TestCase):

    def assert_result(self, assert_method, expect_result_value, actual_result_value, json_path):
        # 根据断言方式断言结果
        if assert_method in ["equal", "eq", "等于"]:
            self.assertEqual(expect_result_value, actual_result_value,
                             msg=f"断言结果=====>【{json_path}】的提取值【{actual_result_value}】，预期等于【{expect_result_value}】，实际不等于")
        elif assert_method in ["notequal", "neq", "不等于"]:
            self.assertNotEqual(expect_result_value, actual_result_value,
                                msg=f"断言结果=====>【{json_path}】的提取值【{actual_result_value}】，预期不等于【{expect_result_value}】，实际等于")
        elif assert_method in ["in", "包含"]:
            self.assertIn(expect_result_value, actual_result_value,
                          msg=f"断言结果=====>【{json_path}】的提取值【{actual_result_value}】，预期包含【{expect_result_value}】，实际不包含")
        elif assert_method in ["not in", "notin", "不包含"]:
            self.assertNotIn(expect_result_value, actual_result_value,
                             msg=f"断言结果=====>【{json_path}】的提取值【{actual_result_value}】，预期不包含【{expect_result_value}】，实际包含")
        elif assert_method in ["Greater", ">", "大于", "GreaterEqual", ">=", "大于等于", "Less", "<", "小于", "LessEqual", "<=",
                               "小于等于"]:
            try:
                expect_result_value = int(expect_result_value)
            except ValueError:
                raise ValueError(f"expect_result_value的值【{expect_result_value}】无法转换为int类型")
            try:
                actual_result_value = int(actual_result_value)
            except ValueError:
                raise ValueError(f"actual_result_value的值【{actual_result_value}】无法转换为int类型")

            if assert_method in ["Greater", ">", "大于"]:
                self.assertGreater(actual_result_value, expect_result_value,
                                   msg=f"断言结果=====>【{json_path}】的提取值【{actual_result_value}】，预期大于【{expect_result_value}】，实际不大于")
            elif assert_method in ["GreaterEqual", ">=", "大于等于"]:
                self.assertGreaterEqual(actual_result_value, expect_result_value,
                                        msg=f"断言结果=====>【{json_path}】的提取值【{actual_result_value}】，预期大于等于【{expect_result_value}】，实际不大于等于")
            elif assert_method in ["Less", "<", "小于"]:
                self.assertLess(actual_result_value, expect_result_value,
                                msg=f"断言结果=====>【{json_path}】的提取值【{actual_result_value}】，预期小于【{expect_result_value}】，实际不小于")
            elif assert_method in ["LessEqual", "<=", "小于等于"]:
                self.assertLessEqual(actual_result_value, expect_result_value,
                                     msg=f"断言结果=====>【{json_path}】的提取值【{actual_result_value}】，预期小于等于【{expect_result_value}】，实际不小于等于")

    @ddt.data(*DDT_DATA)
    @ddt.unpack
    def test_case(self, case_name, description, method, url, headers, data, result_type, expect_result):
        """{description}"""
        ret = requests.request(method, url, headers=headers, data=data)
        ret.encoding = ret.apparent_encoding    # 处理中文异常

        # 处理json结果
        if result_type.lower() == "json":
            actual_result = ret.json()
            logging.info(f"【{case_name}】的执行结果为：{actual_result}")

            # 预期结果不是json格式，抛错
            try:
                expect_result = json.loads(expect_result)
            except JSONDecodeError:
                raise ValueError(f"result_type值为json，但是expect_result的值【{expect_result}】不是有效json格式")

            # 循环判定多个预期结果
            json_paths = expect_result.keys()
            for json_path in json_paths:
                # 校验预期结果的key是否按规定样式填写
                if "$." not in json_path:
                    raise ValueError('expect_result的预期值请按 {"assert_method$jsonPath":"预期值"} 的格式填写')

                split_json_path = json_path.split("$.")
                # 获取断言方式
                assert_method = split_json_path[0].lower()
                if assert_method == '':
                    raise ValueError('expect_result的预期值请按 {"assert_method$jsonPath":"预期值"} 的格式填写')

                # 获取预期结果值
                expect_result_value = expect_result.get(json_path)

                # 根据jsonPath获取实际结果值
                actual_result_value = actual_result
                for k in split_json_path[1].split("."):
                    actual_result_value = actual_result_value.get(k)

                # 断言结果
                self.assert_result(assert_method, expect_result_value, actual_result_value, json_path)

            print(f"请求方式（method）：{method}\n"
                  f"请求地址（url）：{url}\n"
                  f"请求头部（headers）：{headers}\n"
                  f"请求数据（data）：{data}\n"
                  f"结果类型（result_type）：{result_type}\n"
                  f"预期结果（expect_result）：{expect_result}\n"
                  f"实际结果（actual_result）：{actual_result}")
            # try:
            #
            #     actual_ret = ret["weatherinfo"]["city"]
            # except JSONDecodeError:
            #     actual_ret = ret = ret.text
            # self.assertEqual(actual_ret, "成都1")

    # def test_get_weather_info(self):
    #     """  """
    #     ret = requests.request("get", "http://www.weather.com.cn/data/sk/101270101.html")
    #     ret.encoding = ret.apparent_encoding    # 处理中文异常
    #     city = ret.json()["weatherinfo"]["city"]
    #     assert city == "成都"