class BasePage(object):

    def __init__(self, driver):
        self.__driver = driver

    def find_element(self, by, value, times=10, wait_time=1) -> object:
        return self.__driver.until_find_element(by, value, times=10, wait_time=1)