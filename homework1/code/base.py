import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException,\
                                       NoSuchElementException


class BaseCase:
    driver = None

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

    def click_logout(self, locator1, locator2, locator3):
        logout1 = self.delay_check(locator1)
        logout1.click()
        click_retry = 0
        while click_retry < 5:
            try:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator3))
                logout2 = self.delay_check(locator2)
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator2))
                logout2.click()
                break
            except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
                click_retry += 1
        WebDriverWait(self.driver, 10).until(EC.url_to_be("https://target-sandbox.my.com/"))

    def edit_contact_info(self, locator1, query, locator2):
        self.driver.get("https://target-sandbox.my.com/profile/contacts")
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
