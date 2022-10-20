import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver, url='https://target-sandbox.my.com', timeout=30):
        self.driver = driver
        self.url = url
        self.driver.implicitly_wait(timeout)

    def find(self, by, what):
        return self.driver.find_element(by, what)

    def delay_check(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))

    @allure.step("Creating new campaign")
    def create_new_campaign(self, locator):
        create_button = self.delay_check(locator)
        create_button.click()
