import unittest
import requests


class WeatherTest(unittest.TestCase):

    def test_get_weather_info(self):
        """ 测试中国气象台接口数据返回正确性 """
        ret = requests.request("get", "http://www.weather.com.cn/data/sk/101270101.html")
        ret.encoding = ret.apparent_encoding    # 处理中文异常
        city = ret.json()["weatherinfo"]["city"]
        assert city == "成都"
