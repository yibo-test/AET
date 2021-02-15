import time
import logging

from selenium.webdriver import Chrome, Firefox
from selenium.common.exceptions import NoSuchElementException


class Browser(Chrome, Firefox):

    def __init__(self, browser_type="chrome", driver_path=None, *args, **kwargs):
        """
        根据浏览器类型初始化浏览器
        :param browser_type: 浏览器类型，只可传入chrome或firefox
        :param driver_path:指定驱动存放的路径
        """
        # 检查browser_type值是否合法
        if browser_type not in ["chrome", "firefox"]:
            # 不合法报错
            logging.error("browser_type 输入值不为chrome,firefox")
            raise ValueError("browser_type 输入值不为chrome,firefox")

        self.__browser_type = browser_type

        # 根据browser_type值选择对应的驱动
        if self.__browser_type == "chrome":
            if driver_path:
                Chrome.__init__(self, executable_path=f"{driver_path}/chromedriver.exe", *args, **kwargs)
            else:
                Chrome.__init__(self, *args, **kwargs)
        elif self.__browser_type == "firefox":
            if driver_path:
                Firefox.__init__(self, executable_path=f"{driver_path}/geckodriver.exe", *args, **kwargs)
            else:
                Firefox.__init__(self, *args, **kwargs)

    def open_browser(self, url):
        self.get(url)
        self.maximize_window()

    @property
    def browser_name(self):
        return self.capabilities["browserName"]

    @property
    def browser_version(self):
        return self.capabilities["browserVersion"]

    def until_find_element(self, by, value, times=10, wait_time=1):
        """
        用于定位元素
        :param by: 定位元素的方式
        :param value: 定位元素的值
        :param times: 定位元素的重试次数
        :param wait_time: 定位元素失败的等待时间
        :return: 返回定位的元素
        """
        # 检查by的合法性
        if by not in ["id", "xpath", "name", "class", "tag", "text", "partial_text", "css"]:
            # 不合法报错
            logging.error(f"无效定位方式：{by}，请输入：id，xpath, name, class, tag, text, partial_text, css")
            raise ValueError(f"无效定位方式：{by}，请输入：id，xpath, name, class, tag, text, partial_text, css")

        # 定位元素，如果定位失败，增加重试机制
        for i in range(times):
            # 定位元素
            el = None
            try:
                if by == "id":
                    el = super().find_element_by_id(value)
                elif by == "xpath":
                    el = super().find_element_by_xpath(value)
                elif by == "name":
                    el = super().find_element_by_name(value)
                elif by == "class":
                    el = super().find_element_by_class_name(value)
                elif by == "tag":
                    el = super().find_elements_by_tag_name(value)
                elif by == "text":
                    el = super().find_element_by_link_text(value)
                elif by == "partial_text":
                    el = super().find_element_by_partial_link_text(value)
                elif by == "css":
                    el = super().find_element_by_css_selector(value)
            except NoSuchElementException:
                # 如果报错为未找到元素，则重试
                logging.error(f"通过{by}未定位到元素【{value}】，正在进行第{i+1}次重试...")
                time.sleep(wait_time)
            else:
                # 如果成功定位元素则返回元素
                logging.info(""f"通过{by}成功定位元素【{value}】！")
                return el

        # 如果循环完仍为定位到元素，则抛错
        logging.error(f"通过{by}无法定位元素【{value}】，请检查...")
        raise NoSuchElementException(f"通过{by}无法定位元素【{value}】，请检查...")

    def switch_to_new_page(self):
        # 获取老窗口的handle
        old_handle = self.current_window_handle

        handles = self.window_handles
        for handle in handles:
            if handle != old_handle:
                self.switch_to.window(handle)
                break
