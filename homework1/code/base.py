import pytest
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait


class BaseCase:
    driver = None
    name = 'tmlnv@vk.com'
    password = 'qwerty1234'
    wrong_name = "арбуз"
    wrong_password = "re-l-124C41+"
    full_name = "Jay Gatsby"
    profile_url = "https://target-sandbox.my.com/profile/contacts"

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

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

    def click_logout(self, locator1, locator2):
        sleep(3)
        logout1 = self.find(*locator1)
        logout1.click()
        sleep(3)
        logout2 = self.find(*locator2)
        logout2.click()
        sleep(3)

    def edit_contact_info(self, locator1, query, locator2):
        self.driver.get(BaseCase.profile_url)
        self.delay_check(locator1)
        full_name = self.find(*locator1)
        full_name.clear()
        full_name.send_keys(query)
        self.delay_check(locator2)
        save_button = self.find(*locator2)
        save_button.click()

    def check_contact_info(self, locator):
        self.driver.refresh()
        self.delay_check(locator)
        return self.find(*locator).get_attribute('value')

    def page_change(self, locator):
        new_page = self.delay_check(locator)
        new_page.click()
