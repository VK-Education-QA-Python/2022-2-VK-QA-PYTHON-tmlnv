import os
import shutil
import sys

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from ui.pages.login_page import LoginPage
from ui.pages.registration_page import RegistrationPage
from ui.pages.main_page import MainPage
from api.client import ApiClient
from utils.builder import Builder

from ui.credentials import USERNAME, PASSWORD


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@pytest.fixture()
def driver(config, temp_dir):
    browser = config['browser']
    url = config['url']
    headless = config['headless']
    selenoid = config['selenoid']
    vnc = config['vnc']
    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": temp_dir})
    if selenoid:
        capabilities = {
            "browserName": browser,
            "selenoid:options": {
                "enableVNC": False,
                "enableVideo": False
            },
            "additionalNetworks": ["selenoid"]
        }
        if vnc:
            capabilities["selenoid:options"]["enableVNC"] = True
        url = 'http://VK_APP:7777/'
        driver = webdriver.Remote(
            'http://0.0.0.0:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )

    elif browser == 'chrome':
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("window-size=1920,1080")
        driver = webdriver.Chrome(executable_path=ChromeDriverManager(version='107.0.5304.62').install(),
                                  options=options)
    elif browser == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='module', autouse=True)
def cookies():
    api_client = ApiClient(base_url='http://0.0.0.0:7777/login', login=USERNAME, password=PASSWORD)
    api_client.auth()
    cookies = {}
    for cookie in api_client.session.cookies:
        cookies['name'] = 'session'
        cookies['value'] = cookie.value
    return cookies


@pytest.fixture()
def correct_url(driver):
    if 'remote' in repr(driver):
        default_url = 'http://vk_app:7777/'
    else:
        default_url = 'http://0.0.0.0:7777/'
    return default_url


@pytest.fixture()
def new_user():
    builder = Builder()
    new_user_ = builder.app_user()
    return new_user_


@pytest.fixture()
def login_page(driver, correct_url):
    return LoginPage(driver=driver, url=correct_url)


@pytest.fixture()
def registration_page(driver, correct_url):
    return RegistrationPage(driver=driver, url=correct_url)


@pytest.fixture()
def main_page(driver, correct_url):
    return MainPage(driver=driver, url=correct_url)
