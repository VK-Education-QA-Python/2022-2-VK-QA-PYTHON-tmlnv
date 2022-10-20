from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver, url='https://target-sandbox.my.com'):
        self.driver = driver
        self.url = url

    def find(self, by, what):
        return self.driver.find_element(by, what)

    def search_and_input(self, locator1, locator2, query1, query2):
        log_input = self.find(*locator1)
        log_input.clear()
        log_input.send_keys(query1)
        pass_input = self.find(*locator2)
        pass_input.click()
        pass_input.send_keys(query2)

    def delay_check(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))

    def click_login(self, locator):
        elem = self.delay_check(locator)
        return elem.click()

    def login(self, email, password, locator1, locator2, locator3):
        self.search_and_input(locator1, locator2, email, password)
        button = self.find(*locator3)
        button.click()
