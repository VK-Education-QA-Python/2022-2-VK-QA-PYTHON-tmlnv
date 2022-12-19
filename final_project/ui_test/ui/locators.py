from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_USERNAME = (By.ID, 'username')
    LOGIN_PASSWORD = (By.ID, 'password')
    LOGIN_BUTTON = (By.CLASS_NAME, 'uk-button')
    WELCOME_TEXT = (By.CLASS_NAME, 'uk-card-title')
    REGISTRATION_BUTTON = (By.CSS_SELECTOR, "[href='/reg']")
    NOT_REGISTERED_TEXT = (By.CLASS_NAME, 'uk-text-small')
    WARNING_INVALID_USERNAME_OR_PASSWORD = (By.ID, 'flash')


class RegistrationPageLocators:
    REGISTRATION_TITLE_TEXT = (By.CLASS_NAME, 'uk-card-title')
    REGISTRATION_NAME = (By.ID, 'user_name')
    REGISTRATION_SURNAME = (By.ID, 'user_surname')
    REGISTRATION_MIDDLE_NAME = (By.ID, 'user_middle_name')
    REGISTRATION_USERNAME = (By.ID, 'username')
    REGISTRATION_EMAIL = (By.ID, 'email')
    REGISTRATION_PASSWORD = (By.ID, 'password')
    REGISTRATION_PASSWORD_CONFIRM = (By.ID, 'confirm')
    REGISTRATION_TERM_CHECKBOX = (By.ID, 'term')
    REGISTER_BUTTON = (By.ID, 'submit')
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[href='/login']")
    WARNING = (By.ID, 'flash')


class MainPageLocators:
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "[href='/logout']")
    TM_VESRION_NAVBAR = (By.CLASS_NAME, 'uk-navbar-brand')
    HOME_BUTTON_NAVBAR = (By.CSS_SELECTOR, "[href='/']")
    PYTHON_BUTTON_NAVBAR = (By.CSS_SELECTOR, '[href="https://www.python.org/"]')
    PYTHON_HISTORY_DROPDOWN_NAVBAR = (By.CSS_SELECTOR, '[href="https://en.wikipedia.org/wiki/History_of_Python"]')
    ABOUT_FLASK_DROPDOWN_NAVBAR = (By.CSS_SELECTOR, '[href="https://flask.palletsprojects.com/en/1.1.x/#"]')
    LINUX_BUTTON_NAVBAR = (By.CSS_SELECTOR, 'li:nth-child(4).uk-parent')
    DOWNLOAD_CENTOS7_DROPDOWN_NAVBAR = (By.CSS_SELECTOR, '[href="https://getfedora.org/ru/workstation/download/"]')
    NETWORK_BUTTON_NAVBAR = (By.CSS_SELECTOR, 'li:nth-child(5).uk-parent')
    WIRESHARK_NEWS_DROPDOWN_NAVBAR = (By.CSS_SELECTOR, '[href="https://www.wireshark.org/news/"]')
    WIRESHARK_DOWNLOAD_DROPDOWN_NAVBAR = (By.CSS_SELECTOR, '[href="https://www.wireshark.org/#download"]')
    TCDUMP_EXAMPLES_DROPDOWN_NAVBAR = (By.CSS_SELECTOR, '[href="https://hackertarget.com/tcpdump-examples/"]')
    LOGGED_AS = (By.CSS_SELECTOR, '#login-name li:first-child')
    USER = (By.CSS_SELECTOR, '#login-name li:nth-child(2)')
    VK_ID = (By.CSS_SELECTOR, '#login-name li:nth-child(3)')
    WHAT_IS_AN_API = (By.CSS_SELECTOR, '[src="/static/images/laptop.png"]')
    FUTURE_OF_INTERNET = (By.CSS_SELECTOR, '[src="/static/images/loupe.png"]')
    LETS_TALKS_ABOUT_SMTP = (By.CSS_SELECTOR, '[src="/static/images/analytics.png"]')
    FOOTER_TEXT_ABOUT_PYTHON = (By.CSS_SELECTOR, 'footer .uk-text-center p:first-child')
    POWERED_BY_VK_EDUCATION = (By.CSS_SELECTOR, 'footer .uk-text-center p:last-child')
