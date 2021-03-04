import unittest
from libs import ddt


@ddt.ddt
class Api(unittest.TestCase):

    @ddt.data({"case_name": "test_aaa", "v1": 1}, {"case_name": "test_2", "v1": 2})
    @ddt.unpack
    def test_case(self, case_name, v1):
        self.assertEqual(v1, 1)

    def test_get_weather_info(self):
        """ 测试中国气象台接口数据返回正确性 """
        ret = requests.request("get", "http://www.weather.com.cn/data/sk/101270101.html")
        ret.encoding = ret.apparent_encoding    # 处理中文异常
        city = ret.json()["weatherinfo"]["city"]
        assert city == "成都"