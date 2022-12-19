from ui.pages.base_page import BasePage
from ui.locators import LoginPageLocators, MainPageLocators

NAME = 'admin!'
PASSWORD = 'admin'


class LoginPage(BasePage):

    def search_and_input(self, locator_username, locator_password, query1, query2):
        self.clear_and_input(locator_username, query1)
        self.clear_and_input(locator_password, query2)

    def login(self, username, password, locator_username, locator_password, locator_login_button):
        self.search_and_input(locator_username, locator_password, username, password)
        button = self.find(locator_login_button)
        button.click()

    def default_login(self, username=NAME, password=PASSWORD,
                      locator_username=LoginPageLocators.LOGIN_USERNAME,
                      locator_password=LoginPageLocators.LOGIN_PASSWORD,
                      locator_login_button=LoginPageLocators.LOGIN_BUTTON):
        self.login(username, password, locator_username, locator_password, locator_login_button)

    def successful_login(self):
        self.default_login()

    def login_invalid_password(self, invalid_password):
        self.default_login(password=invalid_password)

    def login_invalid_username(self, invalid_username):
        self.default_login(username=invalid_username)

    def login_no_or_short_username(self, invalid_username):
        self.default_login(username=invalid_username, password='')

    def login_no_password(self):
        self.default_login(password='')

    def login_blocked_user(self, blocked_username, blocked_password):
        self.default_login(username=blocked_username, password=blocked_password)

    def click_reg_button(self):
        reg_button = self.delay_check(LoginPageLocators.REGISTRATION_BUTTON)
        reg_button.click()

    def find_warning_invalid_login_pass(self):
        return self.visibility_check(LoginPageLocators.WARNING_INVALID_USERNAME_OR_PASSWORD)

    def find_login_username_field(self):
        return self.delay_check(LoginPageLocators.LOGIN_USERNAME)

    def find_logout_button(self):
        return self.find(MainPageLocators.LOGOUT_BUTTON)
