import allure
from base import BaseCase
import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from api.client import ApiClient
from ui.credentials import USERNAME, NAME, SURNAME, USERNAME_ACCESS0, PASSWORD_ACCESS0

invalid_values = ["привет", 'z6^%*#~', '@aaaaaa', '#12345', '&gthtg', '{}LLLL']
window_sizes = [(1920, 1080), (1366, 768), (360, 640), (414, 896), (1536, 864), (375, 667)]


@pytest.mark.UI
class TestLogin(BaseCase):
    authorize = False

    @allure.step("Testing successful login.")
    def test_successful_login(self):
        """
        Тестирование успешного логина.
        Логин под кредами зарегистрированного юзера. Ожидаемый результат - url меняется на /welcome,
        на открывшейся странице присутствует кнопка логаута.
        """
        self.login_page.successful_login()
        assert self.driver.current_url == self.correct_url + 'welcome/'
        assert self.login_page.find_logout_button()

    @allure.step("Testing login with an invalid password.")
    @pytest.mark.parametrize('invalid_password', invalid_values)
    def test_login_invalid_password(self, invalid_password):
        """
        Параметризованное тестирование логина с невалидным паролем.
        Логин с валидным юзернеймом и невалидным паролем. Ожидаемый результат - появление уведомления
        'Invalid username or password'.
        :param invalid_password:
        """
        self.login_page.login_invalid_password(invalid_password)
        warning = self.login_page.find_warning_invalid_login_pass()
        assert warning.text == 'Invalid username or password'

    @allure.step("Testing login with an invalid username.")
    @pytest.mark.parametrize('invalid_username', invalid_values)
    def test_login_invalid_username(self, invalid_username):
        """
        Параметризованное тестирование логина с невалидным паролем.
        Логин с невалидным юзернеймом. Ожидаемый результат - появление уведомления
        'Invalid username or password'.
        :param invalid_username:
        """
        self.login_page.login_invalid_username(invalid_username)
        warning = self.login_page.find_warning_invalid_login_pass()
        assert warning.text == 'Invalid username or password'

    @allure.step("Testing login without a username or with a username shorter than 6 chars.")
    @pytest.mark.parametrize('invalid_username', ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa', 'NULL'])
    def test_login_no_or_short_username(self, invalid_username):
        """
        Параметризованное тестирование логина с невалидным паролем (короткая длина).
        Логин с невалидным паролем. Ожидаемый результат - логин не проходит, url не меняется,
        на странице отсутствует кнопка логаута.
        :param invalid_username:
        """
        self.login_page.login_no_or_short_username(invalid_username)
        assert self.driver.current_url == self.correct_url
        with pytest.raises(NoSuchElementException):
            assert self.login_page.find_logout_button()

    @allure.step("Testing login without a password.")
    def test_login_no_password(self):
        """
        Тестирование логина без пароля.
        Логин с пустым полем пароля. Ожидаемый результат - логин не проходит, url не меняется,
        на странице отсутствует кнопка логаута.
        """
        self.login_page.login_no_password()
        assert self.driver.current_url == self.correct_url
        with pytest.raises(NoSuchElementException):
            assert self.login_page.find_logout_button()

    @allure.step("Testing registration button.")
    def test_reg_button(self):
        """
        Тестирование кнопки перехода на страницу регистрации.
        Происходит клик по кнопке регистрации. Ожидаемый результат - переход на страницу регистрации, на странице
        есть заголовок 'Registration'.
        """
        self.login_page.click_reg_button()
        reg_text = self.registration_page.find_registration_title()
        assert reg_text.text == 'Registration'

    @allure.step("Testing login for a blocked user.")
    def test_log_blocked(self):
        """
        Тестирование успешного логина.
        Логин под кредами заблокированного юзера. Ожидаемый результат - появление уведомления
        'Ваша учетная запись заблокирована'.
        """
        self.login_page.login_blocked_user(blocked_username='blocked', blocked_password='blocked')
        warning = self.login_page.find_warning_invalid_login_pass()
        assert warning.text == 'Ваша учетная запись заблокирована'

    @allure.step("Testing login with login of spaces.")
    def test_login_spaces_username(self):
        """
        Тестирование логина с юзернеймом из 6 пробелов.
        Происходит попытка авторизации с юзернеймом из пробелов. Ожидаемый результат -
        появление уведомления 'Необходимо указать логин для авторизации'.
        """
        self.login_page.login_invalid_username('      ')
        warning = self.login_page.find_warning_invalid_login_pass()
        assert warning.text == 'Необходимо указать логин для авторизации'

    @allure.step("Testing login with password of spaces.")
    def test_login_spaces_password(self):
        """
        Тестирование логина с паролем из 6 пробелов.
        Происходит попытка авторизации с паролем из пробелов. Ожидаемый результат -
        появление уведомления 'Необходимо указать пароль для авторизации'.
        """
        self.login_page.login_invalid_password('      ')
        warning = self.login_page.find_warning_invalid_login_pass()
        assert warning.text == 'Необходимо указать пароль для авторизации'


@pytest.mark.UI
class TestRegistration(BaseCase):
    authorize = False

    @pytest.fixture(scope='function', autouse=True)
    def go_to_reg_page(self, driver, correct_url):
        driver.get(correct_url + 'reg')

    @allure.step("Testing successful registration.")
    def test_successful_registration(self, new_user):
        """
        Тестирование успешной регистрации.
        Генерируется юзер, происходит регистрации через форму регистрации. Ожидаемый результат - регистрация
        успешна, происходит редирект на страницу /welcome.
        """
        self.registration_page.register_default(new_user.fake_name, new_user.fake_surname,
                                                new_user.fake_middle_name, new_user.fake_username,
                                                new_user.fake_email, new_user.fake_password,
                                                new_user.fake_password)
        self.registration_page.wait_till_url_changes()
        assert self.driver.current_url == self.correct_url + 'welcome/'
        assert self.registration_page.find_user_data()

    @allure.step("Testing successful registration with middle_name.")
    def test_successful_registration_with_middle_name(self, new_user):
        """
        Тестирование регистрации с указанием middle_name.
        Генерируется юзер, происходит регистрации через форму регистрации. Ожидаемый результат - регистрация
        успешна, происходит редирект на страницу /welcome, на странице /welcome в информации о пользователе есть
        отчество.
        """
        middle_name = 'MIDDLE'
        self.registration_page.register_default(new_user.fake_name, new_user.fake_surname,
                                                middle_name, new_user.fake_username,
                                                new_user.fake_email, new_user.fake_password,
                                                new_user.fake_password)
        self.registration_page.wait_till_url_changes()
        assert self.driver.current_url == self.correct_url + 'welcome/'
        registered_user_data = self.registration_page.find_user_data()
        assert middle_name in registered_user_data.text, "Bug. Middle name is not in user information of main page."

    @allure.step("Testing registration of an existing user.")
    def test_registration_of_existing_user(self):
        """
        Тестирование регистрации уже зарегистрированного пользователя.
        Производится попытка регистрации с данными уже существующего юзера. Ожидаемый результат -
        появление уведомления "User already exist".
        """
        self.registration_page.register_existing()
        user_exists = self.registration_page.find_warning()
        assert user_exists.text == "User already exist"

    @allure.step("Testing registration passwords not matching.")
    def test_registration_passwords_not_matching(self, new_user):
        """
        Тестирование регистрации с неверным паролем-подтверждением.
        Производится попытка регистрации с введением пароля-подтверждения, не соответствующего паролю.
        Ожидаемый результат - появление уведомления "Passwords must match".
        """
        self.registration_page.register_default(
            new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, new_user.fake_username,
            new_user.fake_email, new_user.fake_password, '1234567890')
        passwords_match = self.registration_page.find_warning()
        assert passwords_match.text == "Passwords must match"

    @allure.step("Testing registration with no email.")
    def test_registration_no_email(self, new_user):
        """
        Тестирование регистрации с без указания email.
        Производится попытка регистрации без указания email.
        Ожидаемый результат - появление уведомления "Incorrect email length".
        """
        self.registration_page.register_default(
            new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, new_user.fake_username,
            '', new_user.fake_password, new_user.fake_password)
        no_email = self.registration_page.find_warning()
        assert no_email.text == "Incorrect email length"

    @allure.step("Testing registration with incorrect email.")
    @pytest.mark.parametrize('invalid_email', ['aaaaaa', 'aaaaaa@', 'aaaa@aa'])
    def test_registration_incorrect_email(self, new_user, invalid_email):
        """
        Параметризованный тест регистрации с некорректным email.
        Производится попытка регистрации с указанием невалидного email.
        Ожидаемый результат - появление уведомления "Invalid email address".
        :param invalid_email:
        """
        self.registration_page.register_default(
            new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, new_user.fake_username,
            invalid_email, new_user.fake_password, new_user.fake_password)
        no_email = self.registration_page.find_warning()
        assert no_email.text == "Invalid email address"

    @allure.step("Testing registration with no required field.")
    @pytest.mark.parametrize('field', ['name', 'surname', 'username', 'password'])
    def test_registration_no_req_fields(self, new_user, field):
        """
        Параметризованный тест регистрации без указания одного из необходимых полей.
        Производится попытка регистрации без заполнения одного из необходимых полей.
        Ожидаемый результат - отсутсвие редиректа на страницу /welcome, присутсвие на текущей странице
        заголовка регистрации.
        :param field:
        """
        self.registration_page.register_no_req_field(
            field, new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, new_user.fake_username,
            new_user.fake_email, new_user.fake_password, new_user.fake_password)
        with pytest.raises(TimeoutException):
            assert self.registration_page.wait_till_url_changes()
        assert self.registration_page.find_registration_title()

    @allure.step("Testing registration with incorrect username.")
    @pytest.mark.parametrize('invalid_username', ['   123', 'firs t ', ' d 4 5 6 ', 'after   '])
    def test_registration_invalid_username(self, new_user, invalid_username):
        """
        Параметризованный тест регистрации с невалидным юзернеймом с пробелами.
        Производится попытка регистрации с невалидным юзернеймом с пробелами.
        Ожидаемый результат - появление уведомления 'Invalid username or password'.
        :param invalid_username:
        """
        self.registration_page.register_default(
            new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, invalid_username,
            new_user.fake_email, new_user.fake_password, new_user.fake_password)
        warning = self.registration_page.find_warning()
        assert warning.text == 'Invalid username or password', 'Bug with registration of invalid usernames.'

    @allure.step("Testing registration with incorrect password.")
    @pytest.mark.parametrize('invalid_password', ['   123', 'firs t ', ' d 4 5 6 ', 'after   '])
    def test_registration_invalid_password(self, new_user, invalid_password):
        """
        Параметризованный тест регистрации с невалидным паролем с пробелами.
        Производится попытка регистрации с невалидным паролем с пробелами.
        Ожидаемый результат - появление уведомления 'Invalid username or password'.
        :param invalid_password:
        """
        self.registration_page.register_default(
            new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, new_user.fake_username,
            new_user.fake_email, invalid_password, invalid_password)
        warning = self.registration_page.find_warning()
        assert warning.text == 'Invalid username or password', 'Bug. Possible to register with invalid password.'

    @allure.step("Testing registration with username of spaces.")
    def test_registration_username_spaces(self, new_user):
        """
        Тестирование регистрации с юзернеймом из 6 пробелов.
        Производится попытка регистрации с юзернеймом из пробелов.
        Ожидаемый результат - появление уведомления 'Необходимо указать логин для авторизации'.
        """
        self.registration_page.register_default(
            new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, '      ',
            new_user.fake_email, new_user.fake_password, new_user.fake_password)
        warning = self.registration_page.find_warning()
        assert warning.text == 'Необходимо указать логин для авторизации'

    @allure.step("Testing registration with password of spaces.")
    def test_registration_password_spaces(self, new_user):
        """
        Тестирование регистрации с паролем из 6 пробелов.
        Производится попытка регистрации с паролем из пробелов.
        Ожидаемый результат - появление уведомления 'Необходимо указать пароль для авторизации'.
        """
        self.registration_page.register_default(
            new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, new_user.fake_username,
            new_user.fake_email, '      ', '      ')
        warning = self.registration_page.find_warning()
        assert warning.text == 'Необходимо указать пароль для авторизации'

    @allure.step("Testing registration with already registered email.")
    def test_registration_already_registered_email(self, new_user):
        """
        Тестирование регистрации с использованием email уже зарегистрированного юзера.
        Регистрация с использованием email уже существующего юзера. Ожидаемый результат -
        появление уведомления "User already exist".
        """
        self.registration_page.register_default(
            new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, new_user.fake_username,
            'admin@admin.com', new_user.fake_password, new_user.fake_password)
        user_exists = self.registration_page.find_warning()
        assert user_exists.text == "User already exist", 'Bug with registration via already registered email.'

    @allure.step("Testing login page is accessible from registration page.")
    def test_go_to_login(self):
        """
        Тестирование перехода на страницу логина со страницы регистрации.
        Происходит клик по кнопке перехода на страницу логина, смарт ожидание на смену url.
        Ожидаемый результат - переход на страницу /login, присутствие поля логина username на странице.
        """
        self.registration_page.go_to_login()
        self.registration_page.wait_till_url_changes()
        assert self.driver.current_url == self.correct_url + 'login'
        assert self.login_page.find_login_username_field()

    @allure.step("Testing registration without checkbox checked.")
    def test_reg_no_checkbox(self, new_user):
        """
        Тестирование регистрации без проставления галки в чекбоксе.
        Происходит попытка регистрации без проставления чекбокса. Ожидаемый результат -
        таймаут смарт ожидания о смене url, так же присутствие заголовка о регистрации на текущей странице.
        """
        self.registration_page.register_default(
            new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, new_user.fake_username,
            new_user.fake_email, new_user.fake_password, new_user.fake_password, checkbox=False)
        with pytest.raises(TimeoutException):
            self.registration_page.wait_till_url_changes()
        assert self.registration_page.find_registration_title()

    @allure.step("Testing registration with password in Russian with spaces.")
    def test_reg_pass_in_rus(self, new_user):
        """
        Тестирование регистрации с указанием пароля на Русском языке.
        Происходит попытка регистрации с указанием пароля на Русском с пробелами. Ожидаемый результат -
        таймаут смарт ожидания о смене url, так же присутствие заголовка о регистрации на текущей странице.
        """
        password = "па ро ль"
        self.registration_page.register_default(
            new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, new_user.fake_username,
            new_user.fake_email, password, password)
        with pytest.raises(TimeoutException):
            assert self.registration_page.wait_till_url_changes(), \
                "Bug with registration when password is in Russian with spaces."
        assert self.registration_page.find_registration_title()

    @allure.step("Testing registration with required fields of length shorter than required.")
    @pytest.mark.parametrize('username', ['b', 'bb', 'bbb', 'bbbb', 'bbbbb'])
    def test_short_length_username(self, new_user, username):
        """
        Параметризованный тест на регистрацию с указанием юзернейма короче 6 символов.
        Происходит попытка регистрации с указанием юзернейма короче требуемой длины.
        Ожидаемый результат - регистрация не успешна, таймаут смарт ожидания о смене url,
        так же присутствие заголовка о регистрации на текущей странице.
        :param username:
        """
        self.registration_page.register_default(
            new_user.fake_name, new_user.fake_surname, new_user.fake_middle_name, username,
            new_user.fake_email, new_user.fake_password, new_user.fake_password)
        with pytest.raises(TimeoutException):
            assert self.registration_page.wait_till_url_changes()
        assert self.registration_page.find_registration_title()


@pytest.mark.UI
class TestMain(BaseCase):

    @allure.step("Testing main page opens for registered user.")
    def test_main_page_opens(self):
        """
        Тестирование успешного открытия главной страницы для залогиненного юзера.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Ожидаемый результат - текущий url - /welcome, присутствие кнопки логаута на странице.
        """
        assert self.driver.current_url == self.correct_url + 'welcome/'
        assert self.main_page.find_logout_button()

    @allure.step("Testing click on TM Version reloads page.")
    def test_click_on_tn_ver(self):
        """
        Тестирование клика на TM version кнопку.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке TM, ожидаемый результат - страница не изменилась, присутствует кнопка логаута.
        """
        self.main_page.click_on_tm_ver()
        assert self.main_page.find_logout_button()

    @allure.step("Testing click on home button reloads page.")
    def test_click_on_home_button(self):
        """
        Тестирование клика на кнопку home.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке home, ожидаемый результат - страница не изменилась, присутствует кнопка логаута.
        """
        self.main_page.click_home_button()
        assert self.main_page.find_logout_button()

    @allure.step("Testing click on Python button opens Python website.")
    def test_click_python_button(self):
        """
        Тестирование клика на кнопку Python.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке Python, ожидаемый результат - страница 'https://www.python.org/'
        открылась в новой вкладке.
        """
        self.main_page.click_python_button()
        assert self.driver.current_url == 'https://www.python.org/', \
            "Problem with logic. Only Python links are opening in the current tab"

    @allure.step("Testing click on Python History dropdown button opens History of Python page on Wikipedia.")
    def test_click_python_history_button(self):
        """
        Тестирование клика на кнопку Python history.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке Python history, ожидаемый результат -
        страница 'https://en.wikipedia.org/wiki/History_of_Python'
        открылась в новой вкладке.
        """
        self.main_page.click_python_history_button()
        assert self.driver.current_url == 'https://en.wikipedia.org/wiki/History_of_Python', \
            "Problem with logic. Only Python links are opening in the current tab"

    @allure.step("Testing click on About Flask dropdown button opens Flask information page.")
    def test_click_about_flask(self):
        """
        Тестирование клика на кнопку About Flask.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке About Flask, ожидаемый результат -
        страница 'https://flask.palletsprojects.com/en/1.1.x/#'
        открылась в новой вкладке.
        """
        self.main_page.click_about_flask_button()
        assert self.driver.current_url == 'https://flask.palletsprojects.com/en/1.1.x/#'

    @allure.step("Testing click on Linux Centos7 dropdown button opens Fedora download page.")
    def test_click_centos7(self):
        """
        Тестирование клика на кнопку Download Centos7.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке Download Centos7, ожидаемый результат -
        страница 'https://www.centos.org/download/' открылась в новой вкладке.
        """
        self.main_page.click_centos7_button()
        assert self.driver.current_url == 'https://www.centos.org/download/', "Logical error. Ones fedora, not centos7."

    @allure.step("Testing click on Wireshark news dropdown button opens Wireshark news page.")
    def test_click_network_wireshark_news(self):
        """
        Тестирование клика на кнопку Wireshark News.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке Wireshark News, ожидаемый результат -
        страница 'https://www.wireshark.org/news/'
        открылась в новой вкладке.
        """
        self.main_page.click_wireshark_news_button()
        assert self.driver.current_url == 'https://www.wireshark.org/news/'

    @allure.step("Testing click on Wireshark download dropdown button opens Wireshark download page.")
    def test_click_network_wireshark_download(self):
        """
        Тестирование клика на кнопку Wireshark Download.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке Wireshark Download, ожидаемый результат -
        страница 'https://www.wireshark.org/#download'
        открылась в новой вкладке.
        """
        self.main_page.click_wireshark_download_button()
        assert self.driver.current_url == 'https://www.wireshark.org/#download'

    @allure.step("Testing click on TCDUMP examples dropdown button opens TCDUMP examples page.")
    def test_click_network_tcdump_examples(self):
        """
        Тестирование клика на кнопку TCDUMP Examples.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке TCDUMP Examples, ожидаемый результат -
        страница 'https://hackertarget.com/tcpdump-examples/'
        открылась в новой вкладке.
        """
        self.main_page.click_tcdump_examples_button()
        assert self.driver.current_url == 'https://hackertarget.com/tcpdump-examples/'

    @allure.step("Testing username credentials of logged in user are correct on main page.")
    def test_username_credentials(self):
        """
        Тестирование отображения информации о юзернейме пользователя на главной странице.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит проверка информации о юзере в шапке страницы, ожидаемый результат -
        отображается корректный username.
        """
        username = self.main_page.check_username_credentials()
        assert username.text == f'Logged as {USERNAME}'

    @allure.step("Testing name and surname credentials of logged in user are correct on main page.")
    def test_name_surname_credentials(self):
        """
        Тестирование отображения информации об имени и фамилии пользователя на главной странице.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит проверка информации о юзере в шапке страницы, ожидаемый результат -
        отображаются корректные имя и фамилия.
        """
        name_and_surname = self.main_page.check_name_surname_credentials()
        assert name_and_surname.text == f'User: {NAME} {SURNAME}'

    @allure.step("Testing VK ID of logged in user are correct on main page.")
    def test_vk_id(self):
        """
        Тестирование отображения VK ID пользователя на главной странице.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит проверка информации о юзере в шапке страницы, ожидаемый результат -
        отображается VK ID.
        """
        vk_id = self.main_page.check_vk_id()
        assert 'VK ID' in vk_id.text
        assert isinstance(int(vk_id.text.split()[-1]), int)

    @allure.step("Testing logout from main page.")
    def test_logout(self):
        """
        Тестирование логаута.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке логаута, ожидаемый результат -
        url сменился на 'login', так же на странице присутствует поле для юзернейма логина.
        """
        self.main_page.logout()
        assert self.login_page.find_login_username_field()
        assert self.driver.current_url == self.correct_url + 'login'

    @allure.step("Testing click on 'What is an API' img opens Wikipedia API page.")
    def test_click_what_is_an_api(self):
        """
        Тестирование кнопки What Is An API.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке What Is An API, ожидаемый результат -
        страница 'https://en.wikipedia.org/wiki/API'
        открылась в новой вкладке.
        """
        self.main_page.click_what_is_an_api()
        assert self.driver.current_url == 'https://en.wikipedia.org/wiki/API'

    @allure.step("Testing click on 'Future of internet' img opens future of internet article page.")
    def test_click_future_of_internet(self):
        """
        Тестирование кнопки Future Of Internet.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке Future Of Internet, ожидаемый результат -
        страница 'https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/'
        открылась в новой вкладке.
        """
        self.main_page.click_future_of_internet()
        assert self.driver.current_url == \
               'https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/'

    @allure.step("Testing click on 'Lets talk about SMTP' img opens future of internet article page.")
    def test_click_smtp(self):
        """
        Тестирование кнопки Lets talk about SMTP.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Происходит клик по кнопке Lets talk about SMTP, ожидаемый результат -
        страница 'https://ru.wikipedia.org/wiki/SMTP'
        открылась в новой вкладке.
        """
        self.main_page.click_smtp()
        assert self.driver.current_url == 'https://ru.wikipedia.org/wiki/SMTP'

    @allure.step("Testing a fact about Python is on a main page.")
    def test_fact_about_python(self):
        """
        Тестирование факта о Python.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Ожидаемый результат - на странице присутствует факт о Python.
        """
        fact = self.main_page.find_fact_about_python()
        assert isinstance(fact.text, str)

    @allure.step("Testing VK Education copyright is on a main page.")
    def test_vk_edu_copyright(self):
        """
        Тестирование VK Education copyright.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница.
        Ожидаемый результат - на странице присутствует информация о VK Education copyright.
        """
        vk_edu = self.main_page.find_vk_edu_copyright()
        assert isinstance(vk_edu.text, str)
        assert 'Powered by VK Education' in vk_edu.text

    @allure.step("Testing logged in user info is visible in different window sizes.")
    @pytest.mark.parametrize("width, height", window_sizes)
    def test_user_info_visible_different_window_sizes(self, width, height):
        """
        Параметризованный тест отображения на странице информации о пользователе при разных размерах окна.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница. Меняется размер
        окна согласно параметрам. Ожидаемый результат - на странице присутствует информация о пользователе.
        :param width:
        :param height:
        """
        self.driver.set_window_size(width, height)
        assert self.main_page.check_username_credentials()
        assert self.main_page.check_name_surname_credentials()
        assert self.main_page.check_vk_id()

    @allure.step("Testing header is visible in different window sizes.")
    @pytest.mark.parametrize("width, height", window_sizes)
    def test_header_visible_different_window_sizes(self, width, height):
        """
        Параметризованный тест отображения меню шапки на странице при размерах окна.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница. Меняется размер
        окна согласно параметрам. Ожидаемый результат - на странице присутствует меню шапки.
        :param width:
        :param height:
        """
        self.driver.set_window_size(width, height)
        assert self.main_page.check_header_visible() is True, 'Bug. Header is not visible.'

    @allure.step("Testing logout button is visible in different window sizes.")
    @pytest.mark.parametrize("width, height", window_sizes)
    def test_logout_button_visible_different_window_sizes(self, width, height):
        """
        Параметризованный тест отображения кнопки логаута на странице при размерах окна.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница. Меняется размер
        окна согласно параметрам. Ожидаемый результат - на странице присутствует кнопка логаута.
        :param width:
        :param height:
        """
        self.driver.set_window_size(width, height)
        assert self.main_page.find_logout_button()


class TestAccess(BaseCase):

    authorize = False

    @allure.step("Testing access set to 0 while logged in would log out user.")
    def test_active_0(self):
        """
        Тестирование ситуации, когда пользователю выставляется статус access 0 во время сессии.
        Происходит авторизация через API, для авторизованного юзера открывается главная страница,
        пользователю выставляется статус access 0, страница перезагружается.
        Ожидаемый результат - пользователя переводит на страницу логина,
        появление уведомления 'This page is available only to authorized users'.
        """
        self.login_page.default_login(username=USERNAME_ACCESS0, password=PASSWORD_ACCESS0)
        api_client = ApiClient(base_url='http://0.0.0.0:7777/login', login=USERNAME_ACCESS0, password=PASSWORD_ACCESS0)
        api_client.auth()
        api_client.block_user()
        self.driver.refresh()
        warning = self.login_page.find_warning_invalid_login_pass()
        assert warning.text == 'This page is available only to authorized users'
