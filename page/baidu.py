from utils.base_page import BasePage


class HomePage(BasePage):

    @property
    def input_box(self):
        return self.find_element("id", "kw")

    @property
    def search_button(self):
        return self.find_element("id", "su")

    @property
    def news_link(self):
        return self.find_element("xpath", '//*[@id="s-top-left"]/a[1]')


class NewsPage(BasePage):
    @property
    def game_link(self):
        return self.find_element("xpath", '//*[@id="channel-all"]/div/ul/li[10]/a')
