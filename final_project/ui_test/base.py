import os
import allure
import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage


class BaseCase:
    driver = None
    authorize = True
    correct_url = None

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(temp_dir, 'browser.log')
            with open(browser_logs, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            screenshot_path = os.path.join(temp_dir, 'failed.png')
            self.driver.save_screenshot(filename=screenshot_path)
            allure.attach.file(screenshot_path, 'failed.png', allure.attachment_type.PNG)
            with open(browser_logs, 'r') as f:
                allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, request: FixtureRequest, correct_url):
        self.driver = driver
        self.correct_url = correct_url

        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.registration_page: RegistrationPage = (request.getfixturevalue('registration_page'))
        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            self.driver.add_cookie(cookies)

            self.driver.refresh()
            self.main_page: MainPage = (request.getfixturevalue('main_page'))
