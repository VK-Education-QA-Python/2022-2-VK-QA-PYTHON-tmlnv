from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def find(self, locator):
        return self.driver.find_element(*locator)

    def click(self, locator):
        elem = self.delay_check(locator)
        elem.click()

    def delay_check(self, locator):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator))

    def clear_and_input(self, locator, query):
        text_input = self.find(locator)
        text_input.clear()
        text_input.send_keys(query)

    def visibility_check(self, locator):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator))
