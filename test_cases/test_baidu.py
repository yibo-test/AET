import unittest
import time
import logging

from utils.browser import Browser
from page.baidu import HomePage, NewsPage


class Baidu(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = Browser("firefox")
        self.driver.open_browser("http://www.baidu.com")
        logging.info("打开浏览器")
        logging.info(f"浏览器名称:{self.driver.browser_name},浏览器版本:{self.driver.browser_version}")

        self.homepage = HomePage(self.driver)
        self.newspage = NewsPage(self.driver)

    def tearDown(self) -> None:
        self.driver.quit()
        logging.info("关闭浏览器")

    def test_search(self):
        """ 用例1：测试百度搜索框输入selenium能搜索出包含selenium相关的信息 """
        logging.info("用例1：测试百度搜索框输入selenium能搜索出包含selenium相关的信息")

        # 输入搜索信息
        self.homepage.input_box.send_keys("selenium")
        logging.info("输入搜索信息")

        # 点击按钮
        self.homepage.search_button.click()
        logging.info("点击搜索按钮")
        time.sleep(2)

        # 校验搜索结果
        els = self.driver.find_element_by_partial_link_text("selenium")
        self.assertIsNotNone(els)

    def test_access_game_news(self):
        """ 用例2：测试通过百度首页能进入新闻界面的游戏专题 """
        logging.info("用例2：测试通过百度首页能进入新闻界面的游戏专题")

        # 点击新闻链接
        self.homepage.news_link.click()
        logging.info("点击新闻链接")

        # 切换窗口
        self.driver.switch_to_new_page()
        logging.info("切换窗口")

        # 点击游戏链接
        self.newspage.game_link.click()
        logging.info("点击游戏链接")

        # 校验url
        current_url = self.driver.current_url
        self.assertEqual(current_url, "http://news.baidu.com/game")


if __name__ == '__main__':
    unittest.main()