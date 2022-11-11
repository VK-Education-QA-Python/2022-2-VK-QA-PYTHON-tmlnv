from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver, url='https://target-sandbox.my.com'):
        self.driver = driver
        self.url = url

    def find(self, locator):
        return self.driver.find_element(*locator)

    def click(self, locator):
        elem = self.delay_check(locator)
        elem.click()

    def delay_check(self, locator):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator))
