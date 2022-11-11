from ui.pages.base_page import BasePage


class LoginPage(BasePage):

    def search_and_input(self, locator1, locator2, query1, query2):
        self.clear_and_input(locator1, query1)
        self.clear_and_input(locator2, query2)

    def clear_and_input(self, locator, query):
        text_input = self.find(locator)
        text_input.clear()
        text_input.send_keys(query)

    def click_login(self, locator):
        self.click(locator)

    def login(self, email, password, locator1, locator2, locator3):
        self.search_and_input(locator1, locator2, email, password)
        button = self.find(locator3)
        button.click()
