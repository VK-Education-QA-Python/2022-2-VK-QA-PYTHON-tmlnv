from base import BaseCase
import pytest
from ui import basic_locators


@pytest.mark.UI
class TestOne(BaseCase):
    def login_common(self, email=BaseCase.name, password=BaseCase.password):
        self.click_login(locator=basic_locators.LOGIN_BUTTON)
        self.login(email, password, locator1=basic_locators.EMAIL, locator2=basic_locators.PASSWORD,
                   locator3=basic_locators.LOGIN_FORM_BUTTON)

    def test_login(self):
        self.login_common()
        assert self.driver.current_url == 'https://target-sandbox.my.com/dashboard'

    def test_logout(self):
        self.login_common()
        self.click_logout(locator1=basic_locators.LOGOUT_BUTTON, locator2=basic_locators.LOGOUT_BUTTON_2)
        assert self.driver.current_url == 'https://target-sandbox.my.com/'

    def test_login_negative_invalid_email(self):
        self.login_common(email=BaseCase.wrong_name)
        with pytest.raises(AssertionError):
            assert self.driver.current_url == 'https://target-sandbox.my.com/dashboard'

    def test_login_negative_invalid_password(self):
        self.login_common(email=BaseCase.name, password=BaseCase.wrong_password)
        with pytest.raises(AssertionError):
            assert self.driver.current_url == 'https://target-sandbox.my.com/dashboard'

    def test_info_editing(self):
        self.login_common()
        self.edit_contact_info(locator1=basic_locators.FULL_NAME,
                               query=BaseCase.full_name, locator2=basic_locators.SAVE_BUTTON)
        written_name = self.check_contact_info(locator=basic_locators.FULL_NAME)
        assert written_name == BaseCase.full_name

    @pytest.mark.parametrize('locator, check_locator',
                             [(basic_locators.AUDIENCE_BUTTON, basic_locators.AUDIENCE_SEGMENTS),
                              (basic_locators.BILLING_BUTTON, basic_locators.BILLING_PAYER)])
    def test_page_change(self, locator, check_locator):
        self.login_common()
        self.page_change(locator)
        self.delay_check(check_locator)
        assert self.find(*check_locator)
