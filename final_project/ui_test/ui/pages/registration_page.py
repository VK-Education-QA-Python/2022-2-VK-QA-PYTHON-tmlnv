from ui.pages.base_page import BasePage
from ui.locators import RegistrationPageLocators, MainPageLocators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker


fake = Faker()


class RegistrationPage(BasePage):

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.driver = driver
        self.url = url

    def find_registration_title(self):
        return self.visibility_check(RegistrationPageLocators.REGISTRATION_TITLE_TEXT)

    def register(self, locator_name, query_name, locator_surname, query_surname, locator_middle_name, query_middle_name,
                 locator_username, query_username, locator_email, query_email, locator_password, query_password,
                 locator_password_confirm, query_password_confirm, locator_term_checkbox, locator_button,
                 checkbox=True):
        self.clear_and_input(locator_name, query_name)
        self.clear_and_input(locator_surname, query_surname)
        self.clear_and_input(locator_middle_name, query_middle_name)
        self.clear_and_input(locator_username, query_username)
        self.clear_and_input(locator_email, query_email)
        self.clear_and_input(locator_password, query_password)
        self.clear_and_input(locator_password_confirm, query_password_confirm)
        if checkbox:
            self.click(locator_term_checkbox)
        self.click(locator_button)

    @staticmethod
    def get_fake_username():
        fake_username = fake.user_name()
        while True:
            if len(fake_username) in range(6, 17):
                username = fake_username
                break
            else:
                fake_username = fake.user_name()
        return username

    @staticmethod
    def get_fake_password():
        return fake.password()

    def register_default(
            self,
            query_name,
            query_surname,
            query_middle_name,
            query_username,
            query_email,
            query_password,
            query_password_confirm,
            locator_name=RegistrationPageLocators.REGISTRATION_NAME,
            locator_surname=RegistrationPageLocators.REGISTRATION_SURNAME,
            locator_middle_name=RegistrationPageLocators.REGISTRATION_MIDDLE_NAME,
            locator_username=RegistrationPageLocators.REGISTRATION_USERNAME,
            locator_email=RegistrationPageLocators.REGISTRATION_EMAIL,
            locator_password=RegistrationPageLocators.REGISTRATION_PASSWORD,
            locator_password_confirm=RegistrationPageLocators.REGISTRATION_PASSWORD_CONFIRM,
            locator_term_checkbox=RegistrationPageLocators.REGISTRATION_TERM_CHECKBOX,
            locator_button=RegistrationPageLocators.REGISTER_BUTTON,
            checkbox=True
    ):
        self.register(locator_name, query_name, locator_surname, query_surname, locator_middle_name, query_middle_name,
                      locator_username, query_username, locator_email, query_email, locator_password, query_password,
                      locator_password_confirm, query_password_confirm, locator_term_checkbox, locator_button, checkbox
                      )

    def register_existing(self):
        self.register_default(query_name='Arima', query_surname='Kisho', query_middle_name='',
                              query_username='Arima_Kisho', query_email='aaaa@aaaa.com', query_password='1234',
                              query_password_confirm='1234')

    def register_no_req_field(self, field, name, surname, middle_name, username, email, password, password_confirm):
        if field == 'name':
            name = ''
        elif field == 'surname':
            surname = ''
        elif field == 'username':
            username = ''
        elif field == 'password':
            password = ''

        self.register_default(name, surname, middle_name, username, email, password, password_confirm)

    def find_warning(self):
        return self.visibility_check(RegistrationPageLocators.WARNING)

    def wait_till_url_changes(self):
        return WebDriverWait(self.driver, 5).until(EC.url_changes(self.url + 'reg'))

    def find_user_data(self):
        return self.visibility_check(MainPageLocators.USER)

    def go_to_login(self):
        self.click(RegistrationPageLocators.LOGIN_BUTTON)
