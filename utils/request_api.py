import unittest
import logging
import re
import requests
import json
from libs import ddt
from utils.constants import DDT_DATA, GLOBAL_VAR
from json.decoder import JSONDecodeError


def set_global_var(case_name, response_result, variable):
    """
    根据variable的值设置全局变量
    :param case_name: 用于跟踪变量的来源
    :param response_result: 响应结果
    :param variable: 变量名及变量提取路径
    :return:
    """
    # 只有json响应文本才支持提取参数
    if variable is not None:
        print(f"提取变量方式：{variable}")
        # 验证variable参数格式
        try:
            variable = json.loads(variable)
        except JSONDecodeError:
            raise ValueError(f"variable的值【{variable}】不是有效json格式")

        var_result = {}  # 用于显示在报告中
        local_var = {}  # 用于添加到全局变量中

        var_names = variable.keys()
        for var_name in var_names:
            # 校验变量名是否被使用
            if var_name in GLOBAL_VAR:
                source = GLOBAL_VAR.get(var_name).get("source")
                raise ValueError(f"变量名【{var_name}】在用例【{source}】中已被使用")

            # 校验提取变量的路径是否正确
            var_json_path = variable.get(var_name)
            if not var_json_path.startswith("$."):
                raise ValueError(f'variable的【{var_json_path}】提取方式请按 {{"变量名"："$jsonPath"}} 的格式填写')

            # 提取变量值
            response_result_value = response_result
            for k in var_json_path.split("."):
                if "$" not in k:
                    response_result_value = response_result_value.get(k)

            var_result.setdefault(var_name, response_result_value)

            # 将结果添加到临时变量中
            var_info = {"value": response_result_value, "source": case_name}
            local_var.setdefault(var_name, var_info)

        GLOBAL_VAR.update(local_var)
        print(f"提取变量结果：{var_result}")


def conversion_global_var(_str: str, global_var: dict):
    """
    转换用例中使用的变量
    :param _str: 需要转化的内容
    :param global_var: 全局变量
    :return:
    """
    # 校验参数类型
    if not isinstance(_str, str):
        raise ValueError(f"【{_str}】不是str类型")

    if not isinstance(global_var, dict):
        raise ValueError(f"【{global_var}】不是dict类型")

    # 匹配没有引号的结果
    no_quotation_results = re.findall(r"\${\w*}", _str)

    # 匹配有引号的结果
    quotation_results = re.findall(r"['\"]\${\w*}['\"]", _str)

    if len(no_quotation_results) != len(quotation_results):
        raise ValueError(f"【{_str}】中的变量引用部分（${{var_name}}部分），请增加引号(单引号或双引号）")

    if no_quotation_results:
        for result in no_quotation_results:
            var_name = re.search(r"\${(\w*)}", result)
            var_name = var_name.group(1)
            var_value = global_var.get(var_name)
            if var_value is None:
                raise ValueError(f"在全局变量名中{global_var.keys()}中未定义变量：{var_name}")

            _str = _str.replace(result, var_value.get("value"))
    return _str


@ddt.ddt
class Api(unittest.TestCase):

    @ddt.data(*DDT_DATA)
    @ddt.unpack
    def test_case(self, case_id, description, method, url, headers, data, response_type, expect_result, variable):
        """{description}"""
        # 转换变量
        url = conversion_global_var(url, GLOBAL_VAR)
        data = conversion_global_var(data, GLOBAL_VAR)
        headers = conversion_global_var(headers, GLOBAL_VAR)
        if headers:
            # 将headers转化成dict类型
            headers = json.loads(headers)

        # print的内容会在报告中显示
        print(f"请求方式：{method}\n"
              f"请求地址：{url}")
        if headers:
            print(f"请求头部：{headers}")
        if data:
            print(f"请求数据：{data}\n")
        print(f"响应类型：{response_type}\n"
              f"预期结果：{expect_result}")

        # 发送请求
        ret = requests.request(method, url, headers=headers, data=data)
        ret.encoding = ret.apparent_encoding    # 处理中文异常

        # 校验响应类型是否合法
        allow_response_type = ["json", "text", "str"]
        if response_type.lower() not in allow_response_type:
            raise ValueError(f"用例【{case_id}】的response_type的值非法，请输入有效值：{'，'.join(allow_response_type)}")

        # 处理json结果
        if response_type.lower() == "json":
            response_result = ret.json()
            print(f"响应结果：{response_result}")
            logging.info(f"【{case_id}】的执行结果为：{response_result}")

            # 预期结果不是json格式，抛错
            try:
                expect_result = json.loads(expect_result)
            except JSONDecodeError:
                raise ValueError(f"response_type值为json，但是expect_result的值【{expect_result}】不是有效json格式")

            # 循环判定多个预期结果
            json_paths = expect_result.keys()
            for json_path in json_paths:
                # 校验预期结果的key是否按规定样式填写
                if "$." not in json_path:
                    raise ValueError('expect_result的预期值请按 {"assert_method$jsonPath":"预期值"} 的格式填写')

                split_json_path = json_path.split("$.")
                # 获取断言方式
                assert_method = split_json_path[0].lower()

                # 获取预期结果值
                expect_result_value = expect_result.get(json_path)

                # 根据jsonPath获取实际结果值
                response_result_value = response_result
                for k in split_json_path[1].split("."):
                    response_result_value = response_result_value.get(k)

                # 断言结果
                self.assert_json_result(assert_method, expect_result_value, response_result_value, json_path)

            # 设置全局变量
            set_global_var(case_id, response_result, variable)

        # 处理文本类型
        elif response_type.lower() in ["str", "text"]:
            response_result = ret.text
            print(f"响应结果：{response_result}")
            self.assert_text_result(expect_result, response_result)

    def assert_json_result(self, assert_method, expect_result_value, response_result_value, json_path):
        """
        断言预期结果与实际结果，断言方式如下
        等于："equal", "eq", "等于", "="
        不等于："notequal", "neq", "不等于", "!="
        包含："in", "包含"
        不包含："notin", "不包含"
        大于："greater", ">", "大于"
        大于等于："greaterequal", ">=", "大于等于"
        小于："less", "<", "小于"
        小于等于："lessequal", "<=", "小于等于"
        """
        # 根据断言方式断言结果
        if assert_method in ["equal", "eq", "等于", "=", ""]:
            self.assertEqual(expect_result_value, response_result_value,
                             msg=f"断言结果=====>【{json_path}】的提取值【{response_result_value}】，预期等于【{expect_result_value}】，实际不等于")
        elif assert_method in ["notequal", "neq", "不等于", "!="]:
            self.assertNotEqual(expect_result_value, response_result_value,
                                msg=f"断言结果=====>【{json_path}】的提取值【{response_result_value}】，预期不等于【{expect_result_value}】，实际等于")
        elif assert_method in ["in", "包含"]:
            self.assertIn(expect_result_value, response_result_value,
                          msg=f"断言结果=====>【{json_path}】的提取值【{response_result_value}】，预期包含【{expect_result_value}】，实际不包含")
        elif assert_method in ["notin", "不包含"]:
            self.assertNotIn(expect_result_value, response_result_value,
                             msg=f"断言结果=====>【{json_path}】的提取值【{response_result_value}】，预期不包含【{expect_result_value}】，实际包含")
        elif assert_method in ["greater", ">", "大于", "greaterequal", ">=", "大于等于", "less", "<", "小于", "lessequal", "<=",
                               "小于等于"]:
            try:
                expect_result_value = int(expect_result_value)
            except ValueError:
                raise ValueError(f"expect_result_value的值【{expect_result_value}】无法转换为int类型")
            try:
                response_result_value = int(response_result_value)
            except ValueError:
                raise ValueError(f"response_result_value的值【{response_result_value}】无法转换为int类型")

            if assert_method in ["greater", ">", "大于"]:
                self.assertGreater(response_result_value, expect_result_value,
                                   msg=f"断言结果=====>【{json_path}】的提取值【{response_result_value}】，预期大于【{expect_result_value}】，实际不大于")
            elif assert_method in ["greaterequal", ">=", "大于等于"]:
                self.assertGreaterEqual(response_result_value, expect_result_value,
                                        msg=f"断言结果=====>【{json_path}】的提取值【{response_result_value}】，预期大于等于【{expect_result_value}】，实际不大于等于")
            elif assert_method in ["less", "<", "小于"]:
                self.assertLess(response_result_value, expect_result_value,
                                msg=f"断言结果=====>【{json_path}】的提取值【{response_result_value}】，预期小于【{expect_result_value}】，实际不小于")
            elif assert_method in ["lessequal", "<=", "小于等于"]:
                self.assertLessEqual(response_result_value, expect_result_value,
                                     msg=f"断言结果=====>【{json_path}】的提取值【{response_result_value}】，预期小于等于【{expect_result_value}】，实际不小于等于")
        else:
            raise ValueError(f'json响应类型暂不支持【{assert_method}】断言方式！')

    def assert_text_result(self, expect_result, response_result):
        # 如果不是以中括号开头并结尾的预期结果，则当成字符串直接断言
        if not (expect_result.startswith("[") and expect_result.endswith("]")):
            self.assertIn(expect_result, response_result, msg=f"断言结果=====>预期响应结果【{response_result}】包含【{expect_result}】,实际不包含")

        # 如果是中括号开头并结尾的预期结果，则转换成列表进行循环断言
        else:
            re_ret = re.search(r"\[(.+)\]", expect_result).group(1)
            # 如果以中括号开头，又未匹配到数据，则抛错
            if not re_ret:
                raise ValueError(f"预期结果以中括号开头或结尾，但是正则未匹配到信息，请检查！")

            # 如果以 ", "分离数据则以此切割数据
            if ", " in re_ret:
                expect_result_list = re_ret.split(", ")
            elif "," in re_ret:
                expect_result_list = re_ret.split(",")
            else:
                raise ValueError(f"预期结果以中括号开头或结尾，但是数据未以逗号分隔！")

            # 根据切割后的列表，循环断言结果
            for er in expect_result_list:
                self.assertIn(er, response_result, msg=f"断言结果=====>预期响应结果【{response_result}】包含【{er}】,实际不包含")

